from flask import Flask
from flask import request
from flask import Response
import requests
from openai import OpenAI
import os
from multiprocessing import Process


# Give OpenAI Key

client = OpenAI(api_key=os.environ.get("OPENAI_TOKEN"))
token= os.environ.get("TELEGRAM_BOT_TOKEN")
newURL = os.environ.get("HEROKU_URL")


app = Flask(__name__)
# Get BOT Token from telegram



def generate_answer(question):
    completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful healthcare assistant providing information to the layperson."},
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


def process_message(msg):
    chat_id, incoming_que = message_parser(msg)
    answer = generate_answer(incoming_que)
    send_message_telegram(chat_id, answer)

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        print(msg)

        # Create a background process to handle the message
        process = Process(target=process_message, args=(msg,))
        process.start()

        # Return an immediate response to prevent heroku's h12 timeout limited to 30 seconds
        # TG will keep sending responses to server if it doesn't get a 200 response 
        return 'ok'
    else:
        return "<h1>Jack's OPENAI TG BOT</h1>"
    
@app.route('/setwebhook',methods=['GET'])
def set_web_hook():
    response = requests.get(f'https://api.telegram.org/bot6977572928:AAGrqocZSnQVDx3_ZiZ3iKQTkJ7shaGLkB8/setWebhook?url={newURL}')
    print(response)
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False, port=5000)