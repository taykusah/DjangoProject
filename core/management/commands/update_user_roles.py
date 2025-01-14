# core/management/commands/update_user_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile

class Command(BaseCommand):
    help = 'Updates all existing users to have author role'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        count = 0
        for user in users:
            try:
                profile = Profile.objects.get(user=user)
                profile.role = 'author'
                profile.save()
            except Profile.DoesNotExist:
                Profile.objects.create(user=user, role='author')
            count += 1
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {count} users to author role')
        )