from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .behaviour import check_user
from .models import User

@csrf_exempt
def evolution_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            sender_number = data.sender.split('@')[0]

            check_user(sender_number)

            # Aqui você pode fazer o que precisar com os dados recebidos.
            # Por exemplo, salvar no banco de dados ou processar de alguma forma.

            return JsonResponse({"status": "success", "message": "Webhook recebido com sucesso."})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "JSON inválido."}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Método não permitido."}, status=405)
# Create your views here.
