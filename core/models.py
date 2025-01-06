# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = (
        ('user', 'Regular User'),
        ('author', 'Author'),
        ('moderator', 'Moderator'),
        ('admin', 'Administrator'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile - {self.role}"

    @property
    def is_moderator(self):
        return self.role in ['moderator', 'admin']
    
    @property
    def is_author(self):
        return self.role in ['author', 'moderator', 'admin']

# Signal to create/update user profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()