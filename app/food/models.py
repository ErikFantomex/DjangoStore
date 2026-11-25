from django.db import models


class FoodProduct(models.Model):
    """Snapshot of nutrition data returned by Open Food Facts."""

    barcode = models.CharField(max_length=14, unique=True)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    calories_100g = models.FloatField(null=True, blank=True)
    protein_100g = models.FloatField(null=True, blank=True)
    carbohydrates_100g = models.FloatField(null=True, blank=True)
    fat_100g = models.FloatField(null=True, blank=True)
    sugars_100g = models.FloatField(null=True, blank=True)
    nutriscore = models.CharField(max_length=1, blank=True)
    fetched_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name', 'barcode']

    def __str__(self):
        return f'{self.name} ({self.barcode})'
