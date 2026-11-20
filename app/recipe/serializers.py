"""
Serializers for recipe APIs
"""
from rest_framework import serializers
from core.models import Recipe, Tag, Ingredient,Meal,MealPlan

class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient model."""

    class Meta:
        model = Ingredient
        fields = ['id', 'label', 'amount', 'unit', 'user']
        read_only_fields = ['id', 'user']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id', 'meal_id', 'title', 'image_url', 'isMealPrepRecipe',
            'time_minutes', 'price_level', 'tags', 'ingredients',
            'instructions', 'nutritionalInfo'
        ]
        read_only_fields = ['id']

    def validate_time_minutes(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Debe ser al menos un minuto.'
            )
        return value

    def validate_price_level(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                'Debe estar entre 1 y 5.'
            )
        return value

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """Handle getting or creating ingredients as needed"""
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        """Create a recipe"""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']

#clase meal Plan 
class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'
        read_only_fields = ['id', 'user']

class MealPlanSerializer(serializers.ModelSerializer):
    def validate_tracking_days(self, value):
        valid_days = {'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                      'Friday', 'Saturday', 'Sunday'}
        if not isinstance(value, list):
            raise serializers.ValidationError(
                'tracking_days debe ser una lista.'
            )
        invalid = set(value) - valid_days
        if invalid:
            raise serializers.ValidationError(
                f"Días no válidos: {', '.join(sorted(invalid))}"
            )
        return value

    def validate(self, attrs):
        plan_weeks = attrs.get(
            'plan_length_in_weeks',
            getattr(self.instance, 'plan_length_in_weeks', None),
        )
        current_week = attrs.get(
            'current_week',
            getattr(self.instance, 'current_week', None),
        )
        weight = attrs.get(
            'client_weight',
            getattr(self.instance, 'client_weight', None),
        )
        height = attrs.get(
            'client_height',
            getattr(self.instance, 'client_height', None),
        )
        if weight is not None and weight <= 0:
            raise serializers.ValidationError({
                'client_weight': 'Debe ser mayor que cero.'
            })
        if height is not None and height <= 0:
            raise serializers.ValidationError({
                'client_height': 'Debe ser mayor que cero.'
            })
        if plan_weeks is not None and plan_weeks < 1:
            raise serializers.ValidationError({
                'plan_length_in_weeks': 'Debe ser al menos una semana.'
            })
        if current_week is not None and current_week < 1:
            raise serializers.ValidationError({
                'current_week': 'Debe ser al menos la semana uno.'
            })
        if (plan_weeks is not None and current_week is not None
                and current_week > plan_weeks):
            raise serializers.ValidationError({
                'current_week': 'No puede superar la duración del plan.'
            })
        return attrs

    class Meta:
        model = MealPlan
        fields = '__all__'
        read_only_fields = ['id', 'user']
