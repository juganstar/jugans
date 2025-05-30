from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
import logging

class NoSignupSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Auto-link existing users by email
        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass


    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        if not user.username:
            base = user.email.split('@')[0]
            username = base
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base}{counter}"
                counter += 1
            user.username = username
        user.set_unusable_password()
        user.save()
        return user
