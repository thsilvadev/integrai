from .models import User
import json
from django.http import JsonResponse

def add_user(data):
    name = data.get('name')
    phone_number = data.get('phone_number')
    email = data.get('email')

    if User.objects.filter(phone_number=phone_number).exists():
        return JsonResponse({'error': 'User already exists with this phone number'}, status=400)

    user = User.objects.create(name=name, phone_number=phone_number, email=email)
    return JsonResponse({'message': 'User added successfully', 'user_id': user.id})


def check_user(data):
    phone_number = data
    try:
        user = User.objects.get(phone_number=phone_number)
        return JsonResponse({'registered': True, 'name': user.name, 'email': user.email})
    except User.DoesNotExist:
        return JsonResponse({'registered': False})


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