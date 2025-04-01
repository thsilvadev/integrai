from django.db import models
from django.http import JsonResponse

from .actions import send_message, menu


class User(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)  # Agora pode ser nulo e em branco
    phone_number = models.CharField(max_length=20, unique=True, null=False)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)  # Agora pode ser nulo e em branco
    waiting_data = models.CharField(max_length=100, null=True, blank=True)  # Para armazenar o estado
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

    def add_user(self, valid_data):

        try:
            # Desempacotando os dados validados
            name, email = valid_data

            # Atualizar ou salvar o usuário com os novos dados
            self.name = name
            self.email = email
            self.waiting_data = None  # Definindo waiting_data como None, pois agora o usuário foi registrado

            # Salvar as mudanças no banco de dados
            self.save()
            send_message(self.phone_number, "Usuário registrado com sucesso!")
            menu(self, "")
            return JsonResponse({'message': 'User added successfully', 'user_id': self.id})

        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred.', 'details': str(e)}, status=500)

    def delete_user(self, message):
        if message.strip().upper() == "SIM":
            self.delete()
            send_message(self.phone_number, 'Usuário deletado com sucesso.')
            return JsonResponse({'status': 'success', 'message': 'Usuário deletado.'})
        else:
            send_message(self.phone_number, 'Operação cancelada.')
            self.waiting_data = None
            self.save()
            return JsonResponse({'status': 'canceled', 'message': 'Operação cancelada.'})

    def edit_user(self, valid_data):
        try:
            # Desempacotando os dados validados
            name, email = valid_data

            # Atualizar ou salvar o usuário com os novos dados
            self.name = name
            self.email = email
            self.waiting_data = None  # Definindo waiting_data como None, pois agora o usuário foi registrado

            # Salvar as mudanças no banco de dados
            self.save()
            send_message(self.phone_number, "Usuário editado com sucesso!")
            menu(self, "")
            return JsonResponse({'message': 'User edited successfully', 'user_id': self.id})
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred.', 'details': str(e)}, status=500)

# Create your models here.
