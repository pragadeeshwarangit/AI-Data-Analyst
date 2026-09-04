import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "You are a data analyst. Explain what average salary means in one sentence."
        }
    ]
)

print(response["message"]["content"])