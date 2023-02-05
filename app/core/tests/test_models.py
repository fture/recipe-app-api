"""
test for models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='hzdkv@example.com', password='testpass'):

    """create user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """test case for models"""
    
    def test_create_user_with_email_successful(self):
        """test creating a new user with an email is successful"""
        email = 'ychag@example.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
    
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        

    def test_new_user_email_normalized(self):
        """test the email for a new user is normalized"""
        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'], 
            ['ychag@Example.com','ychag@example.com']
        ]
        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, 'test123')

            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """test creating user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'ychag@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """test creating a new recipe"""
        user = get_user_model().objects.create_user(
            'ychag@example.com',
            'test123'
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Test recipe',
            time_minutes=5,
            price=Decimal('5.50'),
            link='https://www.google.com',
            description='Test recipe description'
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """test creating a new tag"""
        user = create_user()

        tag = models.Tag.objects.create(
            user=user,
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """test creating a new ingredient"""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)
    