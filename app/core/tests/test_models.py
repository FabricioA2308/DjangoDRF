# Test for models.
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):

    def test_create_user_with_email_succesfully(self):
        email = "test@example.com"
        password = "testpassword"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_is_normalized(self):
        # Test if email is normalized to newly created user
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_with_empty_email(self):
        # Test creating a user without email
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')

    def test_create_new_superuser(self):
        # Test the creation of a super user.
        super_user = get_user_model().objects.create_superuser(
            email='test123@example.com',
            password='test123'
        )

        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)

    def test_create_recipe(self):
        user = get_user_model().objects.create_user("test@example.com", "testpass123")

        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample recipe title",
            time_minutes=5,
            price=Decimal('5.50'),
            description="Sample recipe description",
        )

        self.assertEqual(str(recipe), recipe.title)
