import re
import ollama
import pandas as pd


def _result(answer, chart=None):
    return {
        "answer": answer,
        "chart": chart
    }


def _find_column(df, text):
    text = text.lower()

    for column in df.columns:
        if str(column).lower() in text:
            return column

    return None


def _format_number(value):
    if pd.isna(value):
        return "N/A"

    if isinstance(value, float):
        return f"{value:,.2f}"

    if isinstance(value, (int, float)):
        return f"{value:,}"

    return str(value)


# ==================================================
# LLM DATASET SUMMARY
# ==================================================

def _create_dataset_summary(df):

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    return f"""
Rows: {len(df)}
Columns: {len(df.columns)}

Columns:
{", ".join(map(str, df.columns))}

Numeric columns:
{", ".join(map(str, numeric_columns))}

Categorical columns:
{", ".join(map(str, categorical_columns))}

Missing values:
{int(df.isnull().sum().sum())}

Duplicate rows:
{int(df.duplicated().sum())}
"""


# ==================================================
# LLM GROUP-BY PLANNER
# ==================================================

def _llm_group_by_plan(df, question):

    summary = _create_dataset_summary(df)

    prompt = f"""
You are a data analysis planning assistant.

DATASET:
{summary}

USER QUESTION:
{question}

Determine whether this question requires a GROUP BY analysis.

If it does, return ONLY this format:

GROUP_BY|metric_column|group_column|operation

Where operation must be one of:
average
sum
count
maximum
minimum

If the question does NOT require group-by analysis, return:

NO

Rules:
- metric_column must be an actual numeric column.
- group_column must be an actual dataset column.
- Never invent column names.
- Do not explain anything.
"""

    try:

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response[
            "message"
        ][
            "content"
        ].strip()

        # Remove accidental markdown
        result = result.replace(
            "```",
            ""
        ).strip()

        return result

    except Exception:

        return "NO"


# ==================================================
# EXECUTE GROUP-BY TOOL
# ==================================================

def _execute_group_by(df, metric, group, operation):

    if metric not in df.columns:
        return None

    if group not in df.columns:
        return None

    if metric not in df.select_dtypes(
        include="number"
    ).columns:

        return None

    grouped = df.groupby(
        group
    )[metric]

    if operation == "average":

        result = grouped.mean()

        operation_name = "Average"

    elif operation == "sum":

        result = grouped.sum()

        operation_name = "Total"

    elif operation == "count":

        result = grouped.count()

        operation_name = "Count"

    elif operation == "maximum":

        result = grouped.max()

        operation_name = "Maximum"

    elif operation == "minimum":

        result = grouped.min()

        operation_name = "Minimum"

    else:

        return None

    result = result.sort_values(
        ascending=False
    )

    lines = []

    for category, value in result.items():

        lines.append(
            f"{category}: {_format_number(value)}"
        )

    return {
        "text": (
            f"{operation_name} {metric} "
            f"by {group}:\n"
            + "\n".join(lines)
        ),
        "labels": [
            str(x)
            for x in result.index
        ],
        "values": [
            round(float(x), 2)
            for x in result.values
        ],
        "operation_name": operation_name
    }


# ==================================================
# MAIN ANALYSIS ENGINE
# ==================================================

def analyze_question(df, question):

    q = question.strip().lower()

    if df.empty:
        return _result(
            "The dataset is empty."
        )

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    # ==================================================
    # GROUP-BY AI TOOL
    # ==================================================

    group_keywords = [
        "by",
        "for each",
        "per",
        "which city",
        "which department",
        "group"
    ]

    if any(
        keyword in q
        for keyword in group_keywords
    ):

        plan = _llm_group_by_plan(
            df,
            question
        )

        if plan.startswith("GROUP_BY|"):

            parts = plan.split("|")

            if len(parts) == 4:

                metric = parts[1].strip()

                group = parts[2].strip()

                operation = parts[3].strip().lower()

                result = _execute_group_by(
                    df,
                    metric,
                    group,
                    operation
                )

                if result:

                    chart = None

                    if any(word in q for word in [
                        "chart",
                        "graph",
                        "plot",
                        "visualize",
                        "visualise",
                        "show"
                    ]):

                        chart = {
                            "type": "bar",
                            "title": (
                                f"{result['operation_name']} "
                                f"{metric} by {group}"
                            ),
                            "labels": result["labels"],
                            "values": result["values"]
                        }

                    return _result(
                        result["text"],
                        chart
                    )

    # ==================================================
    # BASIC QUESTIONS
    # ==================================================

    if any(word in q for word in [
        "how many rows",
        "number of rows",
        "row count",
        "records",
        "employees"
    ]):

        return _result(
            f"The dataset contains {len(df):,} rows."
        )

    if any(word in q for word in [
        "how many columns",
        "number of columns",
        "column count"
    ]):

        return _result(
            f"The dataset contains "
            f"{len(df.columns):,} columns."
        )

    # ==================================================
    # MISSING VALUES
    # ==================================================

    if "missing" in q or "null" in q:

        total = int(
            df.isnull().sum().sum()
        )

        if total == 0:

            return _result(
                "There are no missing values."
            )

        details = ", ".join(
            f"{column}: {count}"
            for column, count
            in df.isnull().sum().items()
            if count > 0
        )

        return _result(
            f"The dataset contains {total} "
            f"missing value(s). {details}"
        )

    # ==================================================
    # DUPLICATES
    # ==================================================

    if "duplicate" in q:

        count = int(
            df.duplicated().sum()
        )

        return _result(
            f"The dataset contains "
            f"{count} duplicate row(s)."
        )

    # ==================================================
    # HIGHEST / LOWEST
    # ==================================================

    for keyword, function, label in [
        (
            "highest",
            "max",
            "highest"
        ),
        (
            "maximum",
            "max",
            "highest"
        ),
        (
            "lowest",
            "min",
            "lowest"
        ),
        (
            "minimum",
            "min",
            "lowest"
        )
    ]:

        if keyword in q:

            column = _find_column(
                df,
                q
            )

            if column in numeric_columns:

                if function == "max":

                    index = df[column].idxmax()

                else:

                    index = df[column].idxmin()

                value = df.loc[
                    index,
                    column
                ]

                answer = (
                    f"The {label} {column} is "
                    f"{_format_number(value)}."
                )

                for candidate in categorical_columns:

                    if df[candidate].nunique() == len(df):

                        person = df.loc[
                            index,
                            candidate
                        ]

                        answer += (
                            f" It belongs to {person}."
                        )

                        break

                return _result(answer)

    # ==================================================
    # AVERAGE
    # ==================================================

    if "average" in q or "mean" in q:

        column = _find_column(
            df,
            q
        )

        if column in numeric_columns:

            return _result(
                f"The average {column} is "
                f"{_format_number(df[column].mean())}."
            )

    # ==================================================
    # MEDIAN
    # ==================================================

    if "median" in q:

        column = _find_column(
            df,
            q
        )

        if column in numeric_columns:

            return _result(
                f"The median {column} is "
                f"{_format_number(df[column].median())}."
            )

    # ==================================================
    # STANDARD DEVIATION
    # ==================================================

    if "standard deviation" in q:

        column = _find_column(
            df,
            q
        )

        if column in numeric_columns:

            return _result(
                f"The standard deviation of "
                f"{column} is "
                f"{_format_number(df[column].std())}."
            )

    # ==================================================
    # UNIQUE
    # ==================================================

    if "unique" in q or "distinct" in q:

        column = _find_column(
            df,
            q
        )

        if column:

            return _result(
                f"{column} contains "
                f"{df[column].nunique():,} unique value(s)."
            )

    # ==================================================
    # CORRELATION
    # ==================================================

    if (
        "correlation" in q
        or "related" in q
        or "relationship" in q
        or "compare" in q
    ):

        mentioned = [
            column
            for column in numeric_columns
            if str(column).lower() in q
        ]

        if len(mentioned) >= 2:

            a = mentioned[0]

            b = mentioned[1]

            correlation = df[
                [a, b]
            ].corr().iloc[0, 1]

            if correlation >= 0.7:
                strength = "strong positive"

            elif correlation >= 0.3:
                strength = "moderate positive"

            elif correlation <= -0.7:
                strength = "strong negative"

            elif correlation <= -0.3:
                strength = "moderate negative"

            else:
                strength = "weak or no"

            return _result(
                f"The correlation between {a} "
                f"and {b} is {correlation:.2f}. "
                f"This indicates a {strength} relationship."
            )

    # ==================================================
    # LLM GENERAL FALLBACK
    # ==================================================

    summary = _create_dataset_summary(df)

    prompt = f"""
You are an AI data analyst.

Dataset summary:
{summary}

User question:
{question}

Answer clearly and concisely.

Do not invent numbers.
Only use information supported by the dataset summary.
If exact analysis is required but the summary is insufficient,
say that detailed analysis is required.
"""

    try:

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response[
            "message"
        ][
            "content"
        ].strip()

        return _result(answer)

    except Exception as error:

        return _result(
            f"I could not analyze that question. "
            f"LLM error: {error}"
        )