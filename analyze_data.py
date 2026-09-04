import pandas as pd

df = pd.read_csv("employees.csv")

print("===== DATASET =====")
print(df)

print("\n===== DATASET INFORMATION =====")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== STATISTICS =====")
print(df.describe())

print("\n===== INSIGHTS =====")

print("Average salary:", df["Salary"].mean())
print("Highest salary:", df["Salary"].max())
print("Lowest salary:", df["Salary"].min())

print("Average age:", df["Age"].mean())
print("Average experience:", df["Experience"].mean())

print("\n===== EMPLOYEES BY CITY =====")
print(df["City"].value_counts())