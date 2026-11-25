from django.db.models import Avg, Count
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from food.models import FoodProduct
from food.serializers import FoodProductSerializer, ImportProductSerializer
from food.services import ProductNotFound, ProductSourceError, fetch_product


class ProductListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=FoodProductSerializer(many=True))
    def get(self, request):
        return Response(FoodProductSerializer(FoodProduct.objects.all(), many=True).data)


class ProductImportView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(request=ImportProductSerializer, responses=FoodProductSerializer)
    def post(self, request):
        serializer = ImportProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        barcode = serializer.validated_data['barcode']
        try:
            fields = fetch_product(barcode)
        except ProductNotFound as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except ProductSourceError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
        product, created = FoodProduct.objects.update_or_create(
            barcode=barcode, defaults=fields,
        )
        return Response(
            FoodProductSerializer(product).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class ProductSummaryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(FoodProduct.objects.aggregate(
            count=Count('id'),
            average_calories=Avg('calories_100g'),
            average_protein=Avg('protein_100g'),
        ))
