from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile

class ProfileModelTest(TestCase):

    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(username='valdemar', password='test123')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_fields_update(self):
        user = User.objects.create_user(username='val', password='pass')
        profile = user.profile
        profile.bio = "Backend developer in the making!"
        profile.phone_number = "+351912345678"
        profile.save()

        updated_profile = Profile.objects.get(user=user)
        self.assertEqual(updated_profile.bio, "Backend developer in the making!")
        self.assertEqual(updated_profile.phone_number, "+351912345678")

    def test_profile_created_if_missing_on_update(self):
        user = User.objects.create_user(username='lost_profile', password='1234')
        Profile.objects.filter(user=user).delete()  # simulate missing profile

        # Trigger post_save again
        user.save()

        self.assertTrue(Profile.objects.filter(user=user).exists())
