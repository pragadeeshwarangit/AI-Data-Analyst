````markdown
# AI Data Analyst

An AI-powered data analysis dashboard that allows users to upload CSV or Excel datasets, automatically analyze their data, visualize statistics, and ask questions using natural language.

The project combines **deterministic data analysis with a local LLM**, using **Pandas for reliable calculations** and **Llama 3.2 through Ollama for natural-language understanding**.

---

## ✨ Features

### 📂 Dataset Analysis

- Upload CSV datasets
- Upload Excel (`.xlsx`) datasets
- Automatic row and column detection
- Automatic data-type detection
- Dataset preview
- Numeric and categorical column identification

### 🧹 Data Quality Analysis

- Missing-value detection
- Missing values by column
- Duplicate-row detection
- Unique-value analysis
- Constant-column detection
- Potential outlier detection using the IQR method

### 📊 Statistical Analysis

For numeric columns, the application can calculate:

- Average
- Median
- Minimum
- Maximum
- Standard deviation

### 💬 Natural Language Analysis

Ask questions about your dataset in plain English.

Example:

```text
How many employees are there?

What is the average salary?

What is the highest salary?

How many unique cities are there?

What is the average salary by city?

Which city has the highest average salary?

Show average salary by city as a chart.
````

### 🤖 AI Integration

The application uses:

* **Llama 3.2**
* **Ollama**
* **Python-based analysis engine**

The LLM is used for natural-language understanding and unsupported questions, while numerical calculations are handled by Pandas.

### 📈 Interactive Visualization

The dashboard can generate interactive charts using **Chart.js**.

---

## 🧠 How It Works

The system uses a hybrid AI + deterministic analysis architecture.

```text
                         ┌──────────────────┐
                         │       User       │
                         │  Upload / Ask    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │      Flask       │
                         │     Backend      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    AI Engine     │
                         │  ai_engine.py    │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
             ┌──────────────┐            ┌──────────────┐
             │    Pandas    │            │   Llama 3.2  │
             │              │            │              │
             │ Calculations │            │ Understanding│
             └──────┬───────┘            └──────┬───────┘
                    │                           │
                    └─────────────┬─────────────┘
                                  ▼
                         ┌──────────────────┐
                         │ Analysis Result  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    Dashboard     │
                         │ Tables + Charts  │
                         └──────────────────┘
```

---

## 🔄 AI Analysis Flow

The project does **not rely entirely on the LLM for numerical calculations**.

Instead, it follows a controlled analysis pipeline.

```text
User Question
      │
      ▼
AI Analysis Engine
      │
      ├── Known analysis?
      │
      ├── YES
      │    │
      │    ▼
      │  Pandas
      │    │
      │    ▼
      │ Actual Result
      │
      └── Unsupported question
           │
           ▼
       Llama 3.2
           │
           ▼
    Natural-language
      interpretation
```

### Grouped Analysis

For questions such as:

> What is the average salary by city?

The system can use the LLM to create a structured analysis plan and then allow Pandas to perform the actual calculation.

```text
User Question
      │
      ▼
Llama 3.2
      │
      ▼
Structured Analysis Plan
      │
      ▼
Pandas
      │
      ▼
Actual Calculation
      │
      ▼
Final Answer / Chart
```

This separation helps keep numerical analysis **deterministic and reliable**, while still using AI where natural-language understanding provides value.

---

## 🛠️ Tech Stack

| Category        | Technologies            |
| --------------- | ----------------------- |
| Backend         | Python, Flask           |
| Data Analysis   | Pandas, OpenPyXL        |
| AI              | Ollama, Llama 3.2       |
| Frontend        | HTML5, CSS3, JavaScript |
| Visualization   | Chart.js                |
| Development     | Visual Studio Code      |
| Version Control | Git, GitHub             |

---

## 📁 Project Structure

```text
AI-Data-Analyst/
│
├── app.py
├── ai_engine.py
├── analyze_data.py
├── create_dataset.py
├── test_ollama.py
├── employees.csv
├── requirements.txt
├── .gitignore
├── README.md
│
└── templates/
    └── index.html
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/pragadeeshwarangit/AI-Data-Analyst.git
```

### 2. Open the project

```bash
cd AI-Data-Analyst
```

### 3. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

### 4. Activate the environment

```powershell
venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Install Ollama

Install Ollama and make sure it is running locally.

Then verify the available models:

```bash
ollama list
```

If Llama 3.2 is not installed:

```bash
ollama pull llama3.2
```

### 7. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 📊 Example Dataset

The repository includes a small employee dataset for testing.

| Name    | Age | City      | Salary | Experience |
| ------- | --: | --------- | -----: | ---------: |
| Arun    |  21 | Chennai   |  35000 |          1 |
| Priya   |  22 | Bangalore |  42000 |          2 |
| Rahul   |  20 | Chennai   |  30000 |          0 |
| Sneha   |  23 | Hyderabad |  50000 |          3 |
| Karthik |  21 | Mumbai    |  38000 |          1 |

---

## 💡 Example Questions

Try asking:

```text
How many employees are there?

What is the average salary?

What is the highest salary?

What is the lowest salary?

How many unique cities are there?

Are there any missing values?

What is the average salary by city?

Which city has the highest average salary?

Show average salary by city as a chart.
```

---

## 🎯 Why This Project?

This project explores how **traditional data-analysis systems can be combined with modern local LLMs**.

Instead of allowing an LLM to perform every calculation, the system separates the responsibilities:

```text
LLM
 ↓
Understand the question

Pandas
 ↓
Perform the calculation

Dashboard
 ↓
Present the result
```

This provides a balance between:

* Natural-language interaction
* Deterministic computation
* Data analysis
* AI-assisted reasoning
* Interactive visualization

---

## 🔮 Future Improvements

Possible future versions could include:

* Advanced natural-language query planning
* Automatic chart selection
* Correlation heatmaps
* Advanced outlier analysis
* Data-cleaning recommendations
* Multiple dataset comparison
* Exportable analysis reports
* Additional file formats
* More powerful local LLM models
* AI-generated executive summaries
* Advanced exploratory data analysis
* Automated report generation

---

## 👨‍💻 Author

**Pragadeeshwaran**

B.Tech Artificial Intelligence & Machine Learning

---

## 📜 License

This project is available for **educational and portfolio purposes**.

```

After pasting:

1. Click **Preview**.
2. Check that the tables look like actual tables and there are **no `[svg]` lines**.
3. Click **Commit changes**.
4. Use commit message:
   `Improve README documentation`

That's the version to use.
```
