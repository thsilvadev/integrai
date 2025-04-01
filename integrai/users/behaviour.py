from .actions import send_message, menu, process_quiz_response
from .models import User
import json
from django.http import JsonResponse
from .utils import is_valid_name_and_email


# PRINCIPAL FUNÇÃO: TRIAGEM DO USUÁRIO/MENSAGEM =>

def check_user(data):
    phone_number = data[0]
    message = data[1]
    print(f'Checkando usuário de número: {phone_number}')

    try:
        # Verificar se o usuário já está registrado:
        user = User.objects.get(phone_number=phone_number)
        print('Usuário registrado.')
        # Processar mensagem:
        process_message(user, phone_number, message)
    except User.DoesNotExist:
        # Caso o usuário não exista, criamos um novo e pedimos o nome e email
        print('Usuário não registrado.')

        # Marcar o usuário como esperando dados
        user = User(phone_number=phone_number, waiting_data="waiting_for_name_and_email")
        user.save()

        send_message(phone_number,
                     "Ainda não te cadastramos. Por favor, envie seu nome e email, separados por uma vírgula.\n\nExemplo: Thiago, thsilva.developer@gmail.com")
        return JsonResponse({'registered': False, 'status': 'waiting_for_name_and_email'})

# FUNÇÕES DE APOIO
# 1 - Processar mensagem => verificar se o usuário estava em outro processo (editando, deletando ou cadastrando-se) e direcionar a mensagem à devida função.
def process_message(user, phone_number, message):
    status = user.waiting_data

    # Se o usuário está registrado, verificamos se ele está aguardando nome e email
    if status == "waiting_for_name_and_email":
        print(f"Usuário está esperando nome e email. Processando a mensagem: {message}")
        # Aqui você pode verificar se a mensagem tem o formato esperado e passar para a função de adicionar usuário
        valid_data = is_valid_name_and_email(message)

        if valid_data:
            # Se os dados forem válidos, adicione o usuário
            user.add_user(valid_data)
            print('Usuário atualizado com sucesso.')
            return
        else:
            send_message(phone_number,
                         'Formato inválido de dados.\n\nCertifique-se de enviar seus dados no formato "{nome},{email}" e tente novamente.')
            return

    elif status == "waiting_for_edit":
        valid_data = is_valid_name_and_email(message)
        if valid_data:
            user.edit_user(valid_data)
            print('Usuário editado com sucesso.')
            return
        else:
            send_message(phone_number, 'Formato inválido. Operação cancelada.')
            user.waiting_data = None
            user.save()
            print('Formato inválido.')
            return

    elif status == "waiting_for_delete_confirmation":
        user.delete_user(message)

    elif status == "waiting_quiz_answer":
        process_quiz_response(user, message)

    # Se o usuário está registrado e não está esperando dados, retorne as informações
    elif status is None:
        print("Chamando o menu...")
        menu(user, message)
        return JsonResponse({'registered': True, 'name': user.name, 'email': user.email})



