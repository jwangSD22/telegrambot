from openai import OpenAI

client = OpenAI(
        api_key="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"

)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "hello!"}
  ]
)


print(completion.choices[0].message.content)
