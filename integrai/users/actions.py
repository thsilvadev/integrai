import os

import requests
from dotenv import load_dotenv

# Carregar as variáveis do .env
load_dotenv()

server_url = os.getenv("SERVER_URL")
instance = os.getenv("INSTANCE")
api_key = os.getenv("API_KEY")

def send_message(number, text):


    url = f"http://{server_url}/message/sendText/{instance}"

    payload = {
        "number": number,
        "options": {
            "delay": 123,
            "presence": "composing",
            "linkPreview": True,
            "quoted": {
                "key": {
                    "remoteJid": "<string>",
                    "fromMe": True,
                    "id": "<string>",
                    "participant": "<string>"
                },
                "message": {"conversation": "<string>"}
            },
            "mentions": {
                "everyOne": True,
                "mentioned": [number]
            }
        },
        "textMessage": {"text": text},
        "isBotMessage": True
    }
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)

def menu(user, message):
    print('apresentando menu ao usuário...')
    print("user: ", user, "\nmessage: ", message)
    if message != '1' or '2':
        send_message(user.phone_number, "Boas vindas ao nosso sistema! O que você gostaria de fazer?\n\nDigite o número conforme a opção desejada:\n\n1 - Editar dados\n\n2 - Deletar conta")
    else:
        send_message(user.phone_number, 'Ainda estamos trabalhando na opcao desejada.')