# AI Data Analyst

An AI-powered data analysis dashboard that allows users to upload CSV or Excel datasets, automatically analyze them, visualize important statistics, and ask questions about their data using natural language.

The project combines deterministic data analysis with an AI layer using Llama 3.2 through Ollama.

---

## Overview

Traditional data analysis often requires users to manually inspect datasets, write queries, calculate statistics, and create visualizations.

AI Data Analyst simplifies this process by providing an interactive dashboard where users can:

- Upload datasets
- Automatically understand their data
- Generate statistical insights
- Detect data-quality issues
- Visualize numeric data
- Ask questions using natural language
- Receive calculated answers using Pandas
- Use an LLM for questions that require natural-language understanding

The project is designed to run locally.

---

## Features

### Dataset Analysis

- CSV file upload
- Excel (`.xlsx`) file upload
- Automatic row and column detection
- Automatic data-type detection
- Dataset preview
- Numeric and categorical column identification

### Data Quality Analysis

- Missing-value detection
- Missing values by column
- Duplicate-row detection
- Unique-value analysis
- Constant-column detection
- Potential outlier detection using the IQR method

### Statistical Analysis

For numeric columns, the application can calculate:

- Average
- Median
- Minimum
- Maximum
- Standard deviation

### Natural Language Data Analysis

Users can ask questions such as:

```text
How many employees are there?

What is the average salary?

What is the highest salary?

How many unique cities are there?

What is the average salary by city?

Which city has the highest average salary?

AI Integration

The application uses:

Llama 3.2
Ollama
A Python-based analysis engine

The LLM is used to understand unsupported or more natural questions, while reliable numerical calculations are handled by Pandas.

Visualization

The dashboard can generate interactive charts using Chart.js.

Architecture


                    ┌──────────────────┐
                    │      User        │
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
                    │   AI Engine      │
                    │  ai_engine.py    │
                    └───────┬──────────┘
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
        ┌────────────────┐    ┌────────────────┐
        │     Pandas     │    │   Llama 3.2    │
        │ Reliable       │    │ Natural        │
        │ calculations   │    │ language       │
        └────────┬───────┘    │ understanding  │
                 │            └───────┬────────┘
                 │                    │
                 └──────────┬─────────┘
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

                   
AI Analysis Flow

The project follows a controlled approach rather than allowing the LLM to directly invent numerical answers.

User Question
      │
      ▼
AI Analysis Engine
      │
      ├── Known analysis?
      │        │
      │       YES
      │        │
      │        ▼
      │      Pandas
      │        │
      │        ▼
      │   Actual Result
      │
      └── Unsupported question
               │
               ▼
           Llama 3.2
               │
               ▼
        Natural-language
          interpretation

For grouped analysis:

User Question
      │
      ▼
Llama 3.2
      │
      ▼
Structured analysis plan
      │
      ▼
Pandas
      │
      ▼
Actual calculation
      │
      ▼
Final answer / chart

This separation helps keep numerical analysis deterministic while using AI where it provides the most value.

Tech Stack
Backend
Python
Flask
Data Analysis
Pandas
OpenPyXL
Artificial Intelligence
Ollama
Llama 3.2
Frontend
HTML5
CSS3
JavaScript
Chart.js
Development
Visual Studio Code
Git
GitHub
Project Structure
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
│
└── templates/
    └── index.html
Installation
1. Clone the repository
git clone https://github.com/pragadeeshwarangit/AI-Data-Analyst.git
2. Open the project
cd AI-Data-Analyst
3. Create a virtual environment

Windows:

python -m venv venv
4. Activate the environment
venv\Scripts\Activate.ps1
5. Install dependencies
pip install -r requirements.txt
6. Install Ollama

Install Ollama and make sure it is running locally.

Then verify that Llama 3.2 is available:

ollama list

If necessary:

ollama pull llama3.2
7. Run the application
python app.py

Open:

http://127.0.0.1:5000
Example Dataset

The repository includes a small employee dataset for testing:

Name	Age	City	Salary	Experience
Arun	21	Chennai	35000	1
Priya	22	Bangalore	42000	2
Rahul	20	Chennai	30000	0
Sneha	23	Hyderabad	50000	3
Karthik	21	Mumbai	38000	1
Example Questions

Try asking:

How many employees are there?
What is the average salary?
What is the highest salary?
What is the lowest salary?
How many unique cities are there?
Are there any missing values?
What is the average salary by city?
Which city has the highest average salary?
Show average salary by city as a chart.
Why This Project?

This project was built to explore how traditional data-analysis systems can be combined with modern local LLMs.

Instead of relying entirely on an LLM for calculations, the system uses:

LLM for understanding

Pandas for computation

This approach provides a better balance between natural-language interaction and reliable numerical analysis.

Future Improvements

Possible future versions could include:

Advanced natural-language query planning
More analysis tools
Automatic chart selection
Correlation heatmaps
Advanced outlier analysis
Data cleaning recommendations
Multiple dataset comparison
Exportable analysis reports
More file formats
More powerful local LLM models
AI-generated executive summaries
Author

Pragadeeshwaran

B.Tech Artificial Intelligence & Machine Learning

License

This project is available for educational and portfolio purposes.
