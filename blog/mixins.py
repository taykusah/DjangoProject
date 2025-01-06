# blog/mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class ModeratorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.profile.is_moderator

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not hasattr(self, 'get_object'):
            return self.request.user.profile.is_author
        obj = self.get_object()
        return self.request.user == obj.author or self.request.user.profile.is_moderator