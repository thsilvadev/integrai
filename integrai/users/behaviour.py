from .actions import send_message, menu
from .models import User
import json
from django.http import JsonResponse

from .utils import is_valid_name_and_email


def check_user(data):
    phone_number = data[0]
    message = data[1]
    print(f'Checkando usuário de número: {phone_number}')

    try:
        # Verificar se o usuário já está registrado
        user = User.objects.get(phone_number=phone_number)
        print('Usuário registrado.')

        # Se o usuário está registrado, verificamos se ele está aguardando nome e email
        if user.waiting_data == "waiting_for_name_and_email":
            print(f"Usuário está esperando nome e email. Processando a mensagem: {message}")
            # Aqui você pode verificar se a mensagem tem o formato esperado e passar para a função de adicionar usuário
            valid_data = is_valid_name_and_email(message)

            if valid_data:
                # Se os dados forem válidos, adicione o usuário
                user.add_user(valid_data)
                return JsonResponse({'status': 'success', 'message': 'Usuário atualizado com sucesso.'})
            else:
                send_message(phone_number, 'Formato inválido de dados. Tente novamente.')
                return JsonResponse({'status': 'error', 'message': 'Formato inválido de dados. Tente novamente.'})

        elif user.waiting_data == "waiting_for_edit":
            valid_data = is_valid_name_and_email(message)
            if valid_data:
                user.edit_user(valid_data)
                return JsonResponse({'status': 'success', 'message': 'Usuário editado com sucesso.'})
            else:
                send_message(phone_number, 'Formato inválido. Operação cancelada.')
                user.waiting_data = None
                user.save()
                return JsonResponse({'status': 'error', 'message': 'Formato inválido.'})

        elif user.waiting_data == "waiting_for_delete_confirmation":
            user.delete_user(message)

        # Se o usuário está registrado e não está esperando dados, retorne as informações
        elif user.waiting_data is None:
            print("Chamando o menu...")
            menu(user, message)
            return JsonResponse({'registered': True, 'name': user.name, 'email': user.email})

    except User.DoesNotExist:
        # Caso o usuário não exista, criamos um novo e pedimos o nome e email
        print('Usuário não registrado.')

        # Marcar o usuário como esperando dados
        user = User(phone_number=phone_number, waiting_data="waiting_for_name_and_email")
        user.save()

        send_message(phone_number,"Ainda não te cadastramos. Por favor, envie seu nome e email, separados por uma vírgula.\n\nExemplo: Thiago, thsilva.developer@gmail.com")
        return JsonResponse({'registered': False, 'status': 'waiting_for_name_and_email'})
