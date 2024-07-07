from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import User
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from ..serializers import UserSerializer
import jwt
from ..utils import *


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                new_user = serializer.save()
                response_obj = {
                    "message": "user created",
                    "user_id": new_user.id,
                    "username": new_user.username,
                    "token": generate_jwt_token(new_user.id),
                }
                return Response(response_obj, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(
                {"error": "user with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValueError:
            return Response(
                {"error": "invalid request body"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                response_object = {
                    "message": "login successful",
                    "user_id": user.id,
                    "username": user.username,
                    "token": generate_jwt_token(user.id),
                }
                return Response(response_object, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except User.DoesNotExist as e:
            return Response(
                {"message": "user does not exist"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except ValueError as e:
            return Response(
                {"message": "invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(e)
            return Response(
                {"message": "something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
