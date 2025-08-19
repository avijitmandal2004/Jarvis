from openai import OpenAI

client = OpenAI(api_key="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")

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant skilled in general tasks like Alexa and Google Cloud."},
        {"role": "user", "content": "What is coding"}
    ]
)

print(completion.choices[0].message.content)

