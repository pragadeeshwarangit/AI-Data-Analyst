from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

from ai_engine import analyze_question


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():
    return render_template("index.html")


# ==================================================
# UPLOAD DATASET
# ==================================================

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("file")

    if file is None or file.filename == "":
        return "No file selected."

    # Support CSV and Excel
    if not file.filename.lower().endswith((".csv", ".xlsx")):
        return "Please upload a CSV or Excel (.xlsx) file."

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(file_path)

    # Read uploaded file
    try:

        if file.filename.lower().endswith(".csv"):
            df = pd.read_csv(file_path)

        else:
            df = pd.read_excel(file_path)

    except Exception as error:

        return f"Could not read the file: {error}"

    if df.empty:
        return "The uploaded dataset is empty."

    # ==================================================
    # BASIC DATASET INFORMATION
    # ==================================================

    row_count = len(df)

    column_count = len(df.columns)

    columns = df.columns.tolist()

    # ==================================================
    # COLUMN TYPES
    # ==================================================

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    # ==================================================
    # MISSING VALUES
    # ==================================================

    missing_values = int(
        df.isnull().sum().sum()
    )

    missing_by_column = {
        column: int(value)
        for column, value in df.isnull().sum().items()
        if value > 0
    }

    # ==================================================
    # DUPLICATE ROWS
    # ==================================================

    duplicate_rows = int(
        df.duplicated().sum()
    )

    # ==================================================
    # NUMERIC STATISTICS
    # ==================================================

    numeric_stats = []

    for column in numeric_columns:

        numeric_stats.append({

            "name": column,

            "average": round(
                float(df[column].mean()), 2
            ),

            "median": round(
                float(df[column].median()), 2
            ),

            "minimum": round(
                float(df[column].min()), 2
            ),

            "maximum": round(
                float(df[column].max()), 2
            ),

            "standard_deviation": round(
                float(df[column].std()), 2
            )

        })

    # ==================================================
    # AUTOMATIC INSIGHTS
    # ==================================================

    insights = []

    insights.append(
        f"The dataset contains {row_count} rows "
        f"and {column_count} columns."
    )

    if numeric_columns:

        insights.append(
            f"The dataset contains "
            f"{len(numeric_columns)} numeric column(s): "
            + ", ".join(numeric_columns)
            + "."
        )

    if categorical_columns:

        insights.append(
            f"The dataset contains "
            f"{len(categorical_columns)} categorical column(s): "
            + ", ".join(categorical_columns)
            + "."
        )

    # ==================================================
    # HIGHEST / LOWEST VALUES
    # ==================================================

    for column in numeric_columns:

        valid_values = df[column].dropna()

        if not valid_values.empty:

            highest_index = valid_values.idxmax()

            lowest_index = valid_values.idxmin()

            highest_value = df.loc[
                highest_index,
                column
            ]

            lowest_value = df.loc[
                lowest_index,
                column
            ]

            insights.append(
                f"Highest {column}: {highest_value}."
            )

            insights.append(
                f"Lowest {column}: {lowest_value}."
            )

    # ==================================================
    # MOST COMMON CATEGORICAL VALUES
    # ==================================================

    for column in categorical_columns:

        valid_values = df[column].dropna()

        if not valid_values.empty:

            most_common = valid_values.mode()[0]

            count = int(
                (df[column] == most_common).sum()
            )

            insights.append(
                f"Most common {column}: "
                f"{most_common} "
                f"({count} occurrence(s))."
            )

    # ==================================================
    # UNIQUE VALUES
    # ==================================================

    for column in columns:

        unique_count = int(
            df[column].nunique()
        )

        insights.append(
            f"{column} contains "
            f"{unique_count} unique value(s)."
        )

    # ==================================================
    # CONSTANT COLUMN DETECTION
    # ==================================================

    for column in columns:

        if df[column].nunique() <= 1:

            insights.append(
                f"Warning: {column} contains "
                f"only one unique value."
            )

    # ==================================================
    # OUTLIER DETECTION
    # ==================================================

    for column in numeric_columns:

        valid_values = df[column].dropna()

        if len(valid_values) >= 4:

            q1 = valid_values.quantile(0.25)

            q3 = valid_values.quantile(0.75)

            iqr = q3 - q1

            lower_limit = q1 - (1.5 * iqr)

            upper_limit = q3 + (1.5 * iqr)

            outliers = valid_values[
                (valid_values < lower_limit)
                | (valid_values > upper_limit)
            ]

            if len(outliers) > 0:

                insights.append(
                    f"Warning: {column} contains "
                    f"{len(outliers)} potential outlier(s)."
                )

            else:

                insights.append(
                    f"No significant outliers detected "
                    f"in {column}."
                )

    # ==================================================
    # MISSING VALUE INSIGHT
    # ==================================================

    if missing_values == 0:

        insights.append(
            "The dataset has no missing values."
        )

    else:

        insights.append(
            f"The dataset contains "
            f"{missing_values} missing value(s)."
        )

        for column, count in missing_by_column.items():

            insights.append(
                f"{column} has {count} missing value(s)."
            )

    # ==================================================
    # DUPLICATE INSIGHT
    # ==================================================

    if duplicate_rows == 0:

        insights.append(
            "No duplicate rows were detected."
        )

    else:

        insights.append(
            f"{duplicate_rows} duplicate row(s) "
            f"were detected."
        )

    # ==================================================
    # CHART DATA
    # ==================================================

    chart_labels = []

    chart_values = []

    if numeric_columns:

        chart_column = numeric_columns[0]

        chart_labels = (
            df.index.astype(str).tolist()
        )

        chart_values = (
            df[chart_column]
            .fillna(0)
            .tolist()
        )

    else:

        chart_column = ""

    # ==================================================
    # DATASET PREVIEW
    # ==================================================

    preview_rows = (
        df.head(10)
        .fillna("")
        .to_dict(orient="records")
    )

    # ==================================================
    # RENDER DASHBOARD
    # ==================================================

    return render_template(

        "index.html",

        columns=columns,

        rows=preview_rows,

        row_count=row_count,

        column_count=column_count,

        numeric_columns=numeric_columns,

        categorical_columns=categorical_columns,

        missing_values=missing_values,

        missing_by_column=missing_by_column,

        duplicate_rows=duplicate_rows,

        numeric_stats=numeric_stats,

        insights=insights,

        chart_column=chart_column,

        chart_labels=chart_labels,

        chart_values=chart_values,

        dataset_filename=file.filename

    )


# ==================================================
# ASK YOUR DATA
# ==================================================

@app.route("/ask", methods=["POST"])
def ask():

    question = request.form.get(
        "question",
        ""
    ).strip()

    filename = request.form.get(
        "filename",
        ""
    ).strip()

    if not question:
        return jsonify({
            "answer": "Please enter a question.",
            "chart": None
        })

    if not filename:
        return jsonify({
            "answer": "No dataset is currently selected.",
            "chart": None
        })

    # Prevent paths outside uploads/
    filename = os.path.basename(filename)

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    if not os.path.exists(file_path):
        return jsonify({
            "answer": "The dataset could not be found.",
            "chart": None
        })

    # Read dataset
    try:

        if filename.lower().endswith(".csv"):

            df = pd.read_csv(file_path)

        elif filename.lower().endswith(".xlsx"):

            df = pd.read_excel(file_path)

        else:

            return jsonify({
                "answer": "Unsupported dataset format.",
                "chart": None
            })

    except Exception as error:

        return jsonify({
            "answer": f"Could not read the dataset: {error}",
            "chart": None
        })

    # Ask analysis engine
    try:

        result = analyze_question(
            df,
            question
        )

        return jsonify({
            "answer": result.get(
                "answer",
                "No answer generated."
            ),
            "chart": result.get(
                "chart"
            )
        })

    except Exception as error:

        return jsonify({
            "answer": f"Analysis error: {error}",
            "chart": None
        })

# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )