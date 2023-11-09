from openai import OpenAI
import asyncio

client = OpenAI(
        api_key="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"

)

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "what are the top places to visit in san diego?"}
#   ]
# )


# print(completion.choices[0].message.content)


def generate_answer(question):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question}
    ]
    )


    answer = completion.choices[0].message.content
    return answer



print(generate_answer('what is a good place to eat in san diego'))