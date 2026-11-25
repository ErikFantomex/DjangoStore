import json
import math
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


class ProductNotFound(Exception):
    pass


class ProductSourceError(Exception):
    pass


def _nutrient(nutriments, key):
    value = nutriments.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if not math.isfinite(value) or value < 0:
        return None
    return float(value)


def fetch_product(barcode):
    """Fetch one barcode from the fixed external host; return normalized fields."""
    url = f'https://world.openfoodfacts.org/api/v2/product/{barcode}'
    request = Request(
        url + '?fields=code,product_name,brands,nutriments,nutrition_grades,image_front_small_url',
        headers={
            'User-Agent': os.environ.get(
                'OPEN_FOOD_FACTS_USER_AGENT',
                'PortalNutricional/1.0 (educational demo)',
            ),
            'Accept': 'application/json',
        },
    )
    try:
        with urlopen(request, timeout=12) as response:
            payload = json.load(response)
    except HTTPError as exc:
        if exc.code == 404:
            raise ProductNotFound('Producto no encontrado en Open Food Facts.') from exc
        raise ProductSourceError('No se pudo consultar Open Food Facts.') from exc
    except (URLError, TimeoutError, ValueError) as exc:
        raise ProductSourceError('No se pudo consultar Open Food Facts.') from exc

    if not isinstance(payload, dict):
        raise ProductSourceError('Open Food Facts devolvió una respuesta inesperada.')
    if payload.get('status') != 1 or not isinstance(payload.get('product'), dict):
        raise ProductNotFound('Producto no encontrado en Open Food Facts.')

    product = payload['product']
    nutriments = product.get('nutriments') or {}
    if not isinstance(nutriments, dict):
        nutriments = {}
    name = str(product.get('product_name') or '').strip()[:255]
    if not name:
        name = f'Producto {barcode}'
    grade = str(product.get('nutrition_grades') or '').lower()
    image_url = product.get('image_front_small_url')
    if isinstance(image_url, str) and len(image_url) <= 500:
        try:
            parsed = urlsplit(image_url)
            if parsed.scheme != 'https' or parsed.netloc != 'images.openfoodfacts.org':
                image_url = ''
        except ValueError:
            image_url = ''
    else:
        image_url = ''
    return {
        'name': name,
        'brand': str(product.get('brands') or '')[:255],
        'image_url': image_url,
        'calories_100g': _nutrient(nutriments, 'energy-kcal_100g'),
        'protein_100g': _nutrient(nutriments, 'proteins_100g'),
        'carbohydrates_100g': _nutrient(nutriments, 'carbohydrates_100g'),
        'fat_100g': _nutrient(nutriments, 'fat_100g'),
        'sugars_100g': _nutrient(nutriments, 'sugars_100g'),
        'nutriscore': grade if grade in 'abcde' and len(grade) == 1 else '',
    }
