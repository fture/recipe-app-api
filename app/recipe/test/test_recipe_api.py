""" Test for recipe API"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer



RECIPES_URL = reverse('recipe:recipe-list')


def create_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00,
        'link': 'https://www.example.com/',
        'description': 'Sample recipe description'
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)

def detail_url(recipe_id):
    """Return recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])





class PublicRecipeApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RECIPES_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTests(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'ychag@example.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test retrieving recipes for user"""
        other_user = get_user_model().objects.create_user(
            'envkt@example.com',
            'testpass'
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_get_recipe_detail(self):
        """Test get recipe detail"""

        recipe = create_recipe(user=self.user)
        
        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe"""

        payload = {
            'title': 'Sample reciped',
            'time_minutes': 10,
            'price': Decimal(5.50),
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key),value)
        self.assertEqual(recipe.title, payload['title'])

    def test_create_recipe_with_tags(self):
        """test creating a recipe with tags"""
        payload = {
            'title': 'Sample recipe with tags',
            'time_minutes': 10,
            'price': Decimal(5.50),
            'tags': [{'name': 'Vegan'},{'name': 'Dessert'}]
        }
        res = self.client.post(RECIPES_URL, payload,format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.filter(user=self.user,)
        self.assertEqual(recipe.count(), 1)
        recipe = recipe.first()
        self.assertEqual(recipe.tags.count(), 2)
        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name=tag['name'],
                user=self.user
            ).exists()
            self.assertTrue(exists)

    def test_create_recipe_with_exist_tags(self):
        """test creating a recipe with exist tags"""
        tag_indian = Tag.objects.create(user=self.user, name='Indian')

        payload = {
            'title': 'Sample recipe with tags',
            'time_minutes': 10,
            'price': Decimal(5.50),
            'tags': [{'name': 'Vegan'},{'name': 'Indian'}]
        }

        res = self.client.post(RECIPES_URL, payload,format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipe.count(), 1)
        recipe = recipe.first()
        self.assertEqual(recipe.tags.count(), 2)
        self.assertIn(tag_indian, recipe.tags.all())
        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name=tag['name'],
                user=self.user
            ).exists()
        
        self.assertTrue(exists)
    
    def test_create_tag_on_update(self):
        """Test creating tag update"""
        recipe = create_recipe(user=self.user)
        
        payload = {'tags': [{'name': 'Vegan'}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload,format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_tag = Tag.objects.get(user=self.user, name='Vegan')
        self.assertIn(new_tag, recipe.tags.all())

    def test_update_recipre_assigned_tag(self):
        """Test updating a recipe with assigned tag"""
        tag_breakfast = Tag.objects.create(user=self.user, name='Breakfast')
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag_breakfast)
        
        tag_lunch = Tag.objects.create(user=self.user, name='Lunch')
        payload = {'tags': [{'name': 'Lunch'}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload,format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_lunch, recipe.tags.all())
        self.assertNotIn(tag_breakfast, recipe.tags.all())
    
    def test_clear_recipe_tags(self):
        """test clear recipe tags"""
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag)
        
        payload = {'tags': []}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload,format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 0)
