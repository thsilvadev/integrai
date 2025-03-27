from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone_number = data.get("phone_number")
            name = data.get("name")

            if not phone_number or not name:
                return JsonResponse({"error": "Missing number or name"}, status=400)

            if User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({"error": "User already exists"}, status=400)

            user = User.objects.create(phone_number=phone_number, name=name)
            return JsonResponse({"message": "User registered successfully", "user_id": user.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)

def check_user(request):
    if request.method == "GET":
        phone_number = request.GET.get("phone_number")

        if not phone_number:
            return JsonResponse({"error": "Missing phone_number"}, status=400)

        # Check if user exists
        user_exists = User.objects.filter(phone_number=phone_number).exists()

        return JsonResponse({"exists": user_exists})

    return JsonResponse({"error": "Only GET allowed"}, status=405)

# Create your views here.
