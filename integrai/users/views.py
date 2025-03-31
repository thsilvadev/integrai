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
            print(data)  # Verifique o que está sendo recebido exatamente

            if data.get('event') == 'messages.upsert':
                # Verificar se a mensagem foi enviada pelo próprio número (fromMe: True)
                is_from_me = data.get('data', {}).get('key', {}).get('fromMe')

                # Se a mensagem foi enviada pelo próprio número, ignore
                if is_from_me:
                    print(f"Ignorando mensagem enviada por mim mesmo.")
                    return JsonResponse({"status": "ignored", "message": "Mensagem enviada por seu número, ignorando."})

                # Pegando o remoteJid de forma segura
                remote_jid = data.get('data', {}).get('key', {}).get('remoteJid', '')

                if not remote_jid:
                    return JsonResponse({"status": "error", "message": "remoteJid não encontrado."}, status=400)

                # Agora vamos extrair o número antes do '@'
                sender_number = remote_jid.split('@')[0]
                message = data['data']['message']['conversation']
                check_user([sender_number, message])

                # Aqui você pode fazer o que precisar com os dados recebidos.
                # Por exemplo, salvar no banco de dados ou processar de alguma forma.

            return JsonResponse({"status": "success", "message": "Webhook recebido com sucesso."})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "JSON inválido."}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Método não permitido."}, status=405)
# Create your views here.
