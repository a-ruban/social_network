from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Like
from .serializers import UserSerializer, ProfileSerializer, PostSerializer, LikesSerializer


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def put(self, request):
        user_data = request.data

        user_serializer = UserSerializer(data=user_data)
        profile_serializer = ProfileSerializer(data=user_data)

        if user_serializer.is_valid(raise_exception=True) and profile_serializer.is_valid(raise_exception=True):
            user_serializer.create(user_data)
            validated_data = user_serializer.validated_data
            return Response(validated_data, status=status.HTTP_201_CREATED)

        return Response(data={'error': 'Invalid data provided.'}, status=status.HTTP_400_BAD_REQUEST)


class PostView(CreateModelMixin, GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def put(self, request):
        return self.create(request)


class LikesView(GenericAPIView, CreateModelMixin, DestroyModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikesSerializer

    def put(self, request, post_id):
        return self.create(request)

    def delete(self, request, post_id):
        return self.destroy(request)

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, partial=True, **kwargs)

    def get_object(self):
        return Like.objects.get(user_id=self.request.user.id, post_id=self.kwargs.get('post_id'))
