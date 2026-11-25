from django.urls import path

from food.views import ProductImportView, ProductListView, ProductSummaryView


urlpatterns = [
    path('products/', ProductListView.as_view(), name='food-products'),
    path('products/import/', ProductImportView.as_view(), name='food-import'),
    path('summary/', ProductSummaryView.as_view(), name='food-summary'),
]
