"""VIews for the recipre API"""
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe API"""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action =='list':
            return serializers.RecipeSerializer # list 즉  resipeserializer를 반환

        return self.serializer_class # detail serializer를 반환

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)
        
    
class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """Manage tags in the database"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """filter queryset to authenticated user only""" 
        return self.queryset.filter(user=self.request.user).order_by('-name')


class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,mixins.UpdateModelMixin, mixins.DestroyModelMixin):

    """Manage ingredients in the database"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """filter queryset to authenticated user only""" 
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
