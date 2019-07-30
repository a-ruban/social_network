from rest_framework import serializers
from rest_framework_simplejwt.state import User

from social_network.models import Profile, Post, Like


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['status', 'bio']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        bio = validated_data.pop('bio', None)
        status = validated_data.pop('status', None)
        user = User.objects.create_user(**validated_data)

        Profile.objects.create(
            bio=bio,
            status=status,
            user=user,
        )
        return user


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ['text', 'title', 'user', 'id']

    def create(self, validated_data):
        current_user = self.context.get('request').user

        return Post.objects.create(user=current_user, **validated_data)


class LikesSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = Like
        fields = ['network', 'post']

    def create(self, validated_data):
        post_id = self.context.get('view').kwargs.get('post_id')
        user = self.context.get('request').user

        return Like.objects.create(post_id=post_id, user=user, **validated_data)
