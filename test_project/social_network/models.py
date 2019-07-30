from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    status = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=300, null=True, blank=True)


class Post(models.Model):
    user = models.ForeignKey(User, null=True, blank=False, on_delete=models.SET_NULL, related_name='posts')
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.title


class Like(models.Model):
    class Meta:
        unique_together = [['post', 'user']]

    networks = (
        ('VK', 'VK'),
        ('Facebook', 'Facebook'),
        ('local', 'local'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    network = models.CharField(choices=networks, default='local', max_length=100)

@receiver(pre_save, sender=Like)
def check_owner(sender, instance, *args, **kwargs):
    post_owner = instance.post.user.id
    like_owner = instance.user.id

    if post_owner == like_owner:
        raise ValidationError('Users cannot like their own posts')
