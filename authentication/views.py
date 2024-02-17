from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializers
from .models import User
from rest_framework import status
from django.contrib import auth
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout



class RegisterView(APIView):
  def post (self, request):
    # Ensure that the 'username' field is present and not empty
    username = request.data.get('username', '')
    if not username:
      return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if a user with the same username already exists
    if User.objects.filter(username=username).exists():
      return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)

    
    # Save the user
    serializer.save()

    return Response(serializer.data)




class LoginView(APIView):
    def post(self, request):
        # Extracting username and password from the request data
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        # Check if the user exists

        if User.objects.filter(username=username).exists():
            # User exists, check if the password is correct
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                print(user)
                return Response({"hello":user }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Password is wrong"}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({"message": "No such user found"}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    

    def post(self, request):
        # Log the user out
        logout(request)
        return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)