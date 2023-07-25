from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model,authenticate, login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()
@api_view(['GET','POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        phone_number = request.data['phone_number']
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password, phone_number=phone_number)
            print('created')
            return redirect('login')  # Redirect to the login page after successful sign-up
        else:
            print('already exists')
            return render(request, 'signup.html', {'error': 'Username already exists'})
    return render(request, 'signup.html')
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response_data, status=200)  # Redirect to a home page or any other desired page after login
    else:
        return Response({'error': 'Invalid credentials'}, status=401)