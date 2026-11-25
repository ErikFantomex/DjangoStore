from rest_framework import serializers

from food.models import FoodProduct


class FoodProductSerializer(serializers.ModelSerializer):
    source_url = serializers.SerializerMethodField()

    class Meta:
        model = FoodProduct
        fields = [
            'id', 'barcode', 'name', 'brand', 'image_url', 'calories_100g',
            'protein_100g', 'carbohydrates_100g', 'fat_100g',
            'sugars_100g', 'nutriscore', 'fetched_at', 'source_url',
        ]

    def get_source_url(self, obj):
        return f'https://world.openfoodfacts.org/product/{obj.barcode}'


class ImportProductSerializer(serializers.Serializer):
    barcode = serializers.RegexField(r'^\d{8,14}$', max_length=14)
