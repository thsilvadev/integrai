import os
import random

import requests
from django.http import JsonResponse
from dotenv import load_dotenv


from .utils import ranking



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
    if message == '1':  # Editar usuário
        user.waiting_data = "waiting_for_edit"
        user.save()
        send_message(user.phone_number, "Por favor, envie seu novo nome e email, separados por uma vírgula.")
        return JsonResponse({'status': 'waiting_for_edit'})

    elif message == '2':  # Deletar usuário
        user.waiting_data = "waiting_for_delete_confirmation"
        user.save()
        send_message(user.phone_number, "Tem certeza que deseja deletar seu cadastro? Responda com SIM para confirmar.")
        return JsonResponse({'status': 'waiting_for_delete_confirmation'})

    elif message == '3':
        start_quiz(user) # Iniciar o quiz
        user.waiting_data = "waiting_quiz_answer"
        user.save()

    elif message == '4':
        show_ranking = ranking()
        send_message(user.phone_number, show_ranking)
        menu(user, "")

    else:
        menu_message = (
            "Opa! Tudo bem? Por enquanto só operamos um simples CRUD.\n\n"
            "Digite o número conforme a opção desejada:\n\n"
            "1 - Editar dados ✏️\n\n"
            "2 - Deletar conta ❌\n\n"
            "3 - Quiz 🧩\n\n"
            "4 - Ranking 🏆"
        )
        send_message(user.phone_number, menu_message)
        return JsonResponse({'status': 'invalid_option'})


def start_quiz(user):
    from .models import QuizQuestion
    # Obtém os IDs das perguntas já respondidas pelo usuário
    answered_ids = user.answered_quiz_questions.split(",") if user.answered_quiz_questions else []

    # Filtra as perguntas que o usuário ainda não respondeu
    available_questions = QuizQuestion.objects.exclude(id__in=answered_ids)

    if not available_questions.exists():
        send_message(user.phone_number, "Você já respondeu todas as perguntas disponíveis! 🏆")
        user.waiting_data = None
        return

    # Escolhe uma pergunta aleatória
    question = random.choice(available_questions)

    # Aleatoriza as respostas, mantendo a ordem das alternativas A, B, C, D
    options = [
        ('A', question.correct_answer),
        ('B', question.wrong_answer_1),
        ('C', question.wrong_answer_2),
        ('D', question.wrong_answer_3)
    ]

    # Aleatoriza apenas as respostas, mas mantém a ordem das alternativas (A, B, C, D)
    answers = [option[1] for option in options]  # Pega as respostas
    random.shuffle(answers)  # Embaralha as respostas

    # Reatribui as respostas embaralhadas de volta às alternativas fixas
    options = [
        ('A', answers[0]),
        ('B', answers[1]),
        ('C', answers[2]),
        ('D', answers[3])
    ]

    # Agora, precisamos identificar qual alternativa contém a resposta correta
    correct_option = next(letter for letter, answer in options if answer == question.correct_answer)

    # Armazena no usuário a resposta correta da pergunta atual
    user.current_quiz_correct_answer = {
        'resposta_correta': correct_option,  # Armazena a alternativa correta (A, B, C ou D)
        'id_question': question.id
    }
    # Envia a pergunta para o usuário com as opções aleatorizadas
    options_text = "\n".join([f"{letter} - {text}" for letter, text in options])
    send_message(user.phone_number, f"{question.question_text}\n\nOpções:\n{options_text}")

    # Retorna o ID da pergunta e as opções ordenadas para uso posterior
    return


def process_quiz_response(user, message):
    if message.strip().upper() == "SAIR":
        user.waiting_data = None
        user.save()
        send_message(user.phone_number, "Quiz encerrado. Você pode voltar quando quiser! 🚪")
        menu(user, "")
        return


    # Valida se a mensagem é uma opção válida
    valid_options = ['A', 'B', 'C', 'D']
    if message.strip().upper() not in valid_options:
        send_message(user.phone_number, "Entrada inválida! Por favor, responda com A, B, C ou D ou SAIR. Tente novamente.")
        return


    # Verifica se a resposta está correta
    selected_option = message.strip().upper()
    if selected_option == user.current_quiz_correct_answer['resposta_correta']:
        user.quiz_score += 1
        # Marca a pergunta como respondida
        answered_ids = user.answered_quiz_questions.split(",") if user.answered_quiz_questions else []
        answered_ids.append(str(user.current_quiz_correct_answer['id_question']))
        user.answered_quiz_questions = ",".join(answered_ids)
        user.waiting_data = None  # Resposta está sendo processada, limpar estado
        user.save()
        send_message(user.phone_number, "Resposta correta! 🎉 Você ganhou 1 ponto.")
    else:
        # Marca a pergunta como respondida
        answered_ids = user.answered_quiz_questions.split(",") if user.answered_quiz_questions else []
        answered_ids.append(str(user.current_quiz_correct_answer['id_question']))
        user.answered_quiz_questions = ",".join(answered_ids)
        user.waiting_data = None  # Resposta está sendo processada, limpar estado
        user.save()
        send_message(user.phone_number, f"Resposta errada! A resposta correta era: {user.current_quiz_correct_answer['resposta_correta']}. ❌")


