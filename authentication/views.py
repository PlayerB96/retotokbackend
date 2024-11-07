from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from .models import User, Challenge
from .serializer import UserSerializer, ChallengeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password, make_password
from .utils import build_response


class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = (permissions.AllowAny,)  # Corregido aquí


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)  # Corregido aquí

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        password = request.data.get("password")
        hashed_password = make_password(password)
        request.data["password"] = hashed_password
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()


@api_view(["POST"])
def validate_user(request):
    # Obtén las credenciales de la solicitud
    email = request.data.get("email", None)
    password = request.data.get("password", None)

    if email and password:
        # Buscar el usuario por el nombre de usuario
        user = User.objects.filter(email=email).first()
        if user is not None and check_password(password, user.password):
            # Usuario válido
            user_data = {
                "uid": user.uid,
                "fullname": user.fullname,
                "email": user.email,
            }

            return Response(
                build_response("Usuario Correcto", user_data, True),
                status=status.HTTP_200_OK,
            )
        else:
            # Usuario no válido
            error_message = "Credenciales Inválidas"
            if user is None:
                error_message = "Usuario no encontrado"
            return Response(
                build_response(error_message, None, False),
                status=status.HTTP_401_UNAUTHORIZED,
            )
    else:
        return Response(
            {"error": "Credenciales faltantes"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def get_challenges_by_detail_id(request):
    id_detail_challenges = request.data.get("id_detail_challenges")

    if not id_detail_challenges:
        return Response(
            {"error": "ID is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    challenges = Challenge.objects.filter(challenge_detail__id=id_detail_challenges)

    if challenges.exists():
        serializer = ChallengeSerializer(challenges, many=True)
        return Response(serializer.data[0], status=status.HTTP_200_OK)

    return Response(
        {"detail": "No challenges found for the provided id_tb_detail_challenges."},
        status=status.HTTP_404_NOT_FOUND,
    )
