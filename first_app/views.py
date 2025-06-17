from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from .models import Registration, TradingConfiguration, Contact, Franchise
from .serializers import RegistrationSerializer, TradingConfigurationSerializer, ContactSerializer, FranchiseSerializer
import json

# Create your views here.

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            serializer = RegistrationSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                return JsonResponse({
                    'message': 'Registration successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'name': user.name
                    }
                })
            return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            try:
                user = Registration.objects.get(username=username)
                if user.check_password(password):
                    return JsonResponse({
                        'message': 'Login successful',
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'name': user.name
                        }
                    })
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
            except Registration.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def trading_config(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')
            if not user_id:
                return JsonResponse({'error': 'User ID is required'}, status=400)

            # Get all configurations for the user
            configs = TradingConfiguration.objects.filter(user_id=user_id)
            
            # Group configurations by category
            categories = {}
            for config in configs:
                if config.category not in categories:
                    categories[config.category] = []
                categories[config.category].append({
                    'symbol': config.symbol,
                    'value': str(config.value),
                    'enabled': config.enabled
                })
            
            return JsonResponse(categories)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            if not user_id:
                return JsonResponse({'error': 'User ID is required'}, status=400)

            # Delete existing configurations for the user
            TradingConfiguration.objects.filter(user_id=user_id).delete()

            # Create new configurations
            for category, instruments in data.items():
                if category != 'user_id':  # Skip the user_id field
                    for instrument in instruments:
                        TradingConfiguration.objects.create(
                            user_id=user_id,
                            category=category,
                            symbol=instrument['symbol'],
                            value=instrument['value'],
                            enabled=instrument['enabled']
                        )

            return JsonResponse({'message': 'Configuration updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def contact_submit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            serializer = ContactSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({
                    'message': 'Thank you for your message. We will get back to you soon!'
                })
            return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def franchise_submit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            serializer = FranchiseSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({
                    'message': 'Thank you for your interest in becoming an egde-fx franchise! We will contact you soon.'
                })
            return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
