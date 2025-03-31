from .actions import send_message, menu
from .models import User
import json
from django.http import JsonResponse

from .utils import is_valid_name_and_email


def add_user(user, valid_data):
    """
    Atualiza ou adiciona um novo usuário com base nos dados validados.

    :param user: O objeto User já verificado
    :param valid_data: Dados válidos contendo [nome, email]
    """
    try:
        # Desempacotando os dados validados
        name, email = valid_data

        # Atualizar ou salvar o usuário com os novos dados
        user.name = name
        user.email = email
        user.waiting_data = None  # Definindo waiting_data como None, pois agora o usuário foi registrado

        # Salvar as mudanças no banco de dados
        user.save()
        send_message(user.phone_number, "Usuário registrado com sucesso!")
        menu(user, "")
        return JsonResponse({'message': 'User added successfully', 'user_id': user.id})

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred.', 'details': str(e)}, status=500)

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
                add_user(user, valid_data)
                return JsonResponse({'status': 'success', 'message': 'Usuário atualizado com sucesso.'})
            else:
                send_message(phone_number, 'Formato inválido de dados. Tente novamente.')
                return JsonResponse({'status': 'error', 'message': 'Formato inválido de dados. Tente novamente.'})

        # Se o usuário está registrado e não está esperando dados, retorne as informações
        if user.waiting_data is None:
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


def delete_user(data):
    phone_number = data.get('phone_number')
    try:
        user = User.objects.get(phone_number=phone_number)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


def edit_user(data):
    phone_number = data.get('phone_number')
    try:
        user = User.objects.get(phone_number=phone_number)
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.save()
        return JsonResponse({'message': 'User updated successfully'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)