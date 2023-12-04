from openai import OpenAI
import asyncio

client = OpenAI(
        api_key="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"

)


question = input('Type in your question: ')

completion = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "You are a helpful assistant healthcare assistant giving information to a layperson"},
    {"role": "user", "content": question}
  ]
)


print(completion.choices[0].message.content)


