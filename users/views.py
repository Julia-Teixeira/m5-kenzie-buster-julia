from rest_framework.views import APIView, Response, Request
from users.permissions import IsAdminOrOwner
from rest_framework.permissions import (
    IsAuthenticated,
)
from .serializers import UserSerializer
from .models import User
from django.shortcuts import get_object_or_404


class UserView(APIView):
    def post(self, request):
        validate_data = UserSerializer(data=request.data)
        validate_data.is_valid(raise_exception=True)
        data_created = validate_data.save()

        formated_data = UserSerializer(instance=data_created)
        return Response(formated_data.data, 201)


class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get(self, request: Request, user_id: int):
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)

        formated_data = UserSerializer(instance=user)
        return Response(formated_data.data, 200)

    def patch(self, request: Request, user_id: int):
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)

        user_new_data = UserSerializer(user, request.data, partial=True)
        user_new_data.is_valid(raise_exception=True)
        updated_user = user_new_data.save()

        formated_data = UserSerializer(instance=updated_user)
        return Response(formated_data.data, 200)
