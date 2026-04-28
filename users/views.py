from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from .utils import hash_password, verify_password, generate_token, decode_token
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data

            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            #validation
            if username is None or email is None or password is None:
                return Response({"error": "All fields are required"}, status=400)
            
            # check if user exists
            if User.objects.filter(email=email).first():
                return Response({"error": "User already exists"}, status=400)
            
            # hash password
            hashed_password = hash_password(password)

            # create user
            user = User(
                username=username,
                email=email,
                password=hashed_password
            )

            user.save()
            return Response({
                "message": "User created successfully",
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email
                }
            }, status=201)

        except Exception as e:
            return Response({
                "message": "Something went wrong",
                "error": str(e)
            }, status=500)

class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            username = data.get("username")
            password = data.get("password")

            if username is None or password is None:
                return Response ({
                    "message": "All fields are required"
                }, status=400)
            
            user = User.objects(username=username).first()
            if not user:
                return Response({
                    "message": "User does not exist"
                }, status=400)
            
            if not verify_password(password, user.password):
                return Response({
                    "message": "Invalid password"
                }, status=400)
            
            token = generate_token(str(user.id))

            response = Response({
                "message": "Login successful",
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email
                },
                "token": token
            }, status=200)

            response.set_cookie(
                key="token",
                value=token,
                httponly=True,
                secure=False,  # change True in production
                samesite="Strict",
                max_age=60 * 60 * 24
            )

            return response

        except Exception as e:
            return Response({
                "message": "Something went wrong",
                "error": str(e)
            }, status=500)
            
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "user": {
                "id": str(request.user.id),
                "username": request.user.username,
                "email": request.user.email
            }
        })