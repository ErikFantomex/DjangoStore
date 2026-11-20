from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.views import generic
from core.models import Recipe, Tag, Ingredient,Meal,MealPlan
from recipe import serializers


#Vistas del Recipiente
class RecipeListView(generic.ListView):
    template_name = 'recipe/recipe_list.html'
    paginate_by = 100
    queryset = Recipe.objects.all()

recipe_list_view = RecipeListView.as_view()
class RecipeDetailView(generic.DetailView):
    template_name = 'recipe/recipe.detail.html'
    queryset = Recipe.objects.all()

recipe_detail_view = RecipeDetailView.as_view()

#Vistas renderizadas  Meal
class MealListView(generic.ListView):
        template_name = 'meal/meal_detail.html'
        paginate_by = 100
        queryset = Meal.objects.all()

meal_list_view = MealListView.as_view()

class MealDetailView(generic.DetailView):
      template_name = 'meal/meal_detail.html'
      queryset = Meal.objects.all()

meal_detail_view = MealDetailView.as_view()

#vistas Meal plan
class MealPlanListView(generic.ListView):
    template_name = 'mealplan/meal_plan_list.html'
    paginate_by = 100
    queryset = MealPlan.objects.all()

meal_plan_list_view = MealPlanListView.as_view()

class MealPlanDetailView(generic.DetailView):
    template_name = 'mealplan/meal_plan_detail.html'
    queryset = MealPlan.objects.all()

meal_plan_detail_view = MealPlanDetailView.as_view()

# Clase recipe
class RecipeViewSet(viewsets.ModelViewSet):
    """ Vista para gestionar recetas en la base de datos """
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """ Convertir cadena de IDs separados por comas en lista de enteros """
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """ Filtrar recetas por tags, ingredientes y usuario """
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)
        return queryset.filter(user=self.request.user).order_by('-id').distinct()

    def get_serializer_class(self):
        """ Devolver el serializador adecuado según la acción """
        if self.action == 'list':
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """ Guardar el objeto con el usuario asociado """
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=False, url_path='recommend')
    def recommend(self, request):
        """Recomendar recetas por coincidencia con ingredientes seleccionados."""
        ingredients = request.data.get('ingredients', [])
        if isinstance(ingredients, str):
            ingredients = [
                item.strip()
                for item in ingredients.replace(',', ' ').split()
                if item.strip()
            ]
        if not isinstance(ingredients, list):
            return Response(
                {'ingredients': 'Debe ser una lista.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        selected = {
            str(item).strip().lower()
            for item in ingredients
            if str(item).strip()
        }
        if not selected:
            return Response([], status=status.HTTP_200_OK)

        ranked = []
        queryset = self.get_queryset()
        for recipe in queryset.prefetch_related('ingredients'):
            recipe_ingredients = {
                ingredient.label.strip().lower()
                for ingredient in recipe.ingredients.all()
            }
            if not recipe_ingredients:
                continue
            matches = selected & recipe_ingredients
            union = selected | recipe_ingredients
            score = len(matches) / len(union)
            if matches:
                ranked.append((score, len(matches), recipe))

        ranked.sort(key=lambda item: (item[0], item[1]), reverse=True)
        data = serializers.RecipeSerializer(
            [item[2] for item in ranked[:20]],
            many=True,
            context={'request': request},
        ).data
        return Response([
            {
                **recipe_data,
                'match_score': round(ranked[index][0] * 100),
                'matching_ingredients': ranked[index][1],
            }
            for index, recipe_data in enumerate(data)
        ])

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ Subir imagen para la receta """
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filtrar por items asignados a recetas'
            )
        ]
    )
)
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Vista base para los atributos de recetas """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    name_field = 'name'  # por defecto es 'name'

    def get_queryset(self):
        """ Obtener objetos filtrados por usuario y ordenados por campo name_field """
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipes__isnull=False)
        return queryset.filter(user=self.request.user).order_by(f'-{self.name_field}').distinct()

class TagViewSet(BaseRecipeAttrViewSet):
    """ Vista para gestionar etiquetas en la base de datos """
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()

class IngredientViewSet(BaseRecipeAttrViewSet):
    """ Vista para gestionar ingredientes en la base de datos """
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    name_field = 'label'  # para ingredientes, el campo es 'label'

# Meal plan
class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all().order_by('name')
    serializer_class = serializers.MealSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all().order_by('client_name')
    serializer_class = serializers.MealPlanSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
