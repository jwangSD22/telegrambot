from flask import Flask
from flask import request
from flask import Response
import requests
from openai import OpenAI
import os

# Give OpenAI Key

client = OpenAI(api_key=os.environ.get("OPENAI_TOKEN"))
token= os.environ.get("TELEGRAM_BOT_TOKEN")
newURL = os.environ.get("HEROKU_URL")


app = Flask(__name__)
# Get BOT Token from telegram



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


# To Get Chat ID and message which is sent by client
def message_parser(message):
    chat_id = message['message']['chat']['id']
    text = message['message']['text']
    print("Chat ID: ", chat_id)
    print("Message: ", text)
    return chat_id, text


# To send message using "SendMessage" API
def send_message_telegram(chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        print(msg)
        chat_id, incoming_que = message_parser(msg)
        answer = generate_answer(incoming_que)
        send_message_telegram(chat_id, answer)
        
        return 'ok'
    else:
        return "<h1>Something went wrong!</h1>"
    
@app.route('/setwebhook',methods=['GET'])
def set_web_hook():
    response = requests.get(f'https://api.telegram.org/bot6977572928:AAGrqocZSnQVDx3_ZiZ3iKQTkJ7shaGLkB8/setWebhook?url={newURL}')
    print(response)
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False, port=5000)