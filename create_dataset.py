import pandas as pd

data = {
    "Name": ["Arun", "Priya", "Rahul", "Sneha", "Karthik"],
    "Age": [21, 22, 20, 23, 21],
    "City": ["Chennai", "Bangalore", "Chennai", "Hyderabad", "Mumbai"],
    "Salary": [35000, 42000, 30000, 50000, 38000],
    "Experience": [1, 2, 0, 3, 1]
}

df = pd.DataFrame(data)

df.to_csv("employees.csv", index=False)

print("Dataset created successfully!")
print(df)