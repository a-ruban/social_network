from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from social_network.views import SignUpView, PostView, LikesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/signup', SignUpView.as_view(), name='signup'),
    path('api/v1/auth/login', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/v1/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/post/', PostView.as_view(), name='post'),
    path('api/v1/post/<int:post_id>/likes/', LikesView.as_view(), name='Likes'),
]
