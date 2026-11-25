from unicodedata import category, normalize


# Everyday recipes. Amounts describe ingredients for the recipe, not dietary goals.
IDEAS = [
    ('avena', 'Avena con manzana y canela', 12,
     [('Avena', '½', 'taza'), ('Manzana', '1', 'pieza'), ('Leche', '1', 'taza'), ('Canela', '¼', 'cdita')],
     'Calienta la leche con la avena y cocina a fuego bajo hasta que espese. Agrega la manzana en cubos y espolvorea canela.'),
    ('yogur', 'Yogur con plátano y avena', 5,
     [('Yogur natural', '¾', 'taza'), ('Plátano', '1', 'pieza'), ('Avena', '2', 'cdas')],
     'Sirve el yogur en un tazón. Añade el plátano en rodajas y termina con la avena.'),
    ('garbanzo', 'Ensalada de garbanzos', 15,
     [('Garbanzo', '1', 'taza cocida'), ('Pepino', '½', 'pieza'), ('Tomate', '1', 'pieza'), ('Limón', '1', 'pieza')],
     'Escurre los garbanzos cocidos. Corta el pepino y el tomate en cubos, mezcla y añade jugo de limón al gusto.'),
    ('nopal', 'Tacos de nopal y queso panela', 20,
     [('Nopal', '150', 'g'), ('Queso panela', '60', 'g'), ('Tortilla', '2', 'piezas'), ('Tomate', '1', 'pieza')],
     'Asa el nopal en tiras hasta que esté tierno. Calienta las tortillas y rellénalas con nopal, queso y tomate picado.'),
    ('pollo', 'Tazón de arroz con pollo y brócoli', 30,
     [('Pollo', '150', 'g'), ('Arroz', '½', 'taza cruda'), ('Brócoli', '1', 'taza'), ('Zanahoria', '1', 'pieza')],
     'Cuece el arroz según el paquete. Saltea la zanahoria y el brócoli en trozos. Cocina el pollo por completo en una sartén y sírvelo sobre el arroz con las verduras.'),
    ('frijol', 'Tostadas de frijol y aguacate', 15,
     [('Frijol negro', '¾', 'taza cocida'), ('Aguacate', '½', 'pieza'), ('Tortilla', '2', 'piezas'), ('Tomate', '1', 'pieza')],
     'Dora las tortillas en un comal. Machaca los frijoles cocidos y repártelos sobre las tortillas. Termina con rebanadas de aguacate y tomate.'),
    ('huevo', 'Huevos revueltos con espinaca', 12,
     [('Huevo', '2', 'piezas'), ('Espinaca', '1', 'taza'), ('Cebolla', '¼', 'pieza')],
     'Sofríe la cebolla picada, incorpora la espinaca y deja que se ablande. Vierte los huevos batidos y remueve hasta que cuajen.'),
    ('atun', 'Ensalada de atún y aguacate', 10,
     [('Atún', '1', 'lata'), ('Aguacate', '½', 'pieza'), ('Lechuga', '2', 'tazas'), ('Limón', '1', 'pieza')],
     'Escurre el atún. Mezcla con aguacate en cubos y jugo de limón. Sirve sobre la lechuga lavada.'),
    ('lenteja', 'Sopa de lentejas con verduras', 35,
     [('Lenteja', '½', 'taza cruda'), ('Zanahoria', '1', 'pieza'), ('Tomate', '2', 'piezas'), ('Cebolla', '¼', 'pieza')],
     'Enjuaga las lentejas. Sofríe la cebolla y el tomate, añade la zanahoria y las lentejas, cubre con agua y cocina hasta que estén tiernas.'),
    ('quinoa', 'Ensalada de quinoa y pimiento', 25,
     [('Quinoa', '½', 'taza cruda'), ('Pimiento', '½', 'pieza'), ('Pepino', '½', 'pieza'), ('Aceite de oliva', '1', 'cda')],
     'Enjuaga y cuece la quinoa según el paquete. Deja enfriar y mezcla con el pimiento y el pepino picados y el aceite.'),
    ('salmon', 'Salmón al limón con coliflor', 25,
     [('Salmón', '150', 'g'), ('Coliflor', '1', 'taza'), ('Limón', '1', 'pieza'), ('Ajo', '1', 'diente')],
     'Corta la coliflor y mézclala con el ajo. Hornea la coliflor y el salmón hasta que estén cocidos. Sirve con jugo de limón.'),
    ('tofu', 'Tofu con champiñones y jengibre', 20,
     [('Tofu', '150', 'g'), ('Champiñón', '1', 'taza'), ('Pimiento', '½', 'pieza'), ('Jengibre', '1', 'cdita')],
     'Seca el tofu, córtalo en cubos y dóralo en una sartén. Añade el pimiento, los champiñones y el jengibre rallado. Saltea hasta que las verduras estén tiernas.'),
    ('pasta', 'Pasta integral con calabaza', 25,
     [('Pasta integral', '80', 'g'), ('Calabaza', '1', 'pieza'), ('Tomate', '2', 'piezas'), ('Ajo', '1', 'diente')],
     'Cuece la pasta. Saltea el ajo y la calabaza en cubos, agrega el tomate y cocina unos minutos. Mezcla con la pasta escurrida.'),
    ('pavo', 'Sándwich de pavo y pepino', 10,
     [('Pan integral', '2', 'rebanadas'), ('Pavo', '60', 'g cocidos'), ('Pepino', '¼', 'pieza'), ('Lechuga', '2', 'hojas')],
     'Tuesta el pan si lo prefieres. Corta el pepino en rodajas y arma el sándwich con el pavo ya cocido, el pepino y la lechuga.'),
    ('frutas', 'Tazón de mango, fresa y yogur', 10,
     [('Mango', '1', 'pieza'), ('Fresa', '½', 'taza'), ('Yogur natural', '¾', 'taza'), ('Arándano', '¼', 'taza')],
     'Lava las frutas y pela el mango. Córtalas, sírvelas sobre el yogur y añade los arándanos.'),
    ('cottage', 'Pan integral con pera y queso cottage', 8,
     [('Pan integral', '2', 'rebanadas'), ('Pera', '1', 'pieza'), ('Queso cottage', '½', 'taza')],
     'Tuesta el pan y reparte el queso. Corta la pera en rebanadas y acomódalas sobre el pan.'),
    ('pescado', 'Tacos de pescado con aguacate', 25,
     [('Pescado', '150', 'g'), ('Aguacate', '½', 'pieza'), ('Tortilla', '2', 'piezas'), ('Limón', '1', 'pieza')],
     'Cocina el pescado por completo en una sartén. Calienta las tortillas y rellénalas con el pescado, el aguacate y el jugo de limón.'),
    ('haba', 'Ensalada de habas y tomate', 15,
     [('Haba', '1', 'taza cocida'), ('Tomate', '1', 'pieza'), ('Cebolla', '¼', 'pieza'), ('Aceite de oliva', '1', 'cda')],
     'Escurre las habas cocidas. Añade tomate y cebolla picados y mezcla con el aceite.'),
    ('res', 'Salteado de res y verduras', 20,
     [('Carne de res', '150', 'g'), ('Pimiento', '1', 'pieza'), ('Champiñón', '½', 'taza'), ('Cebolla', '¼', 'pieza')],
     'Corta la carne y las verduras en tiras. Cocina la carne, agrega las verduras y saltea hasta que estén tiernas y la carne esté bien cocida.'),
    ('fresca', 'Ensalada fresca de sandía y kiwi', 10,
     [('Sandía', '1', 'taza'), ('Kiwi', '1', 'pieza'), ('Naranja', '1', 'pieza')],
     'Corta la sandía y el kiwi en cubos. Exprime media naranja sobre la fruta y añade la otra mitad en gajos.'),
]

_ALIASES = {
    'jitomate': 'tomate', 'jitomates': 'tomate', 'tomates': 'tomate',
    'banana': 'platano', 'banano': 'platano', 'platanos': 'platano',
    'champinones': 'champinon', 'espinacas': 'espinaca',
    'garbanzos': 'garbanzo', 'lentejas': 'lenteja', 'huevos': 'huevo',
    'tortillas': 'tortilla', 'frijoles negros': 'frijol negro',
    'yogurt natural': 'yogur natural', 'calabacita': 'calabaza',
}


def ingredient_key(label):
    letters = (char for char in normalize('NFD', label.casefold()) if category(char) != 'Mn')
    key = ' '.join(''.join(letters).split())
    return _ALIASES.get(key, key)


def idea_recipes():
    for key, title, minutes, ingredients, instructions in IDEAS:
        yield {
            'recommendation_key': f'idea:{key}',
            'meal_id': key,
            'title': title,
            'description': '',
            'image_url': '',
            'isMealPrepRecipe': False,
            'time_minutes': minutes,
            'price_level': 2,
            'tags': [],
            'ingredients': [
                {'label': label, 'amount': amount, 'unit': unit}
                for label, amount, unit in ingredients
            ],
            'instructions': instructions,
            'nutritionalInfo': {},
        }


def match_recipe(recipe, selected):
    ingredients = {
        ingredient_key(item['label']): item['label'] for item in recipe['ingredients']
    }
    matches = [name for key, name in ingredients.items() if key in selected]
    missing = [name for key, name in ingredients.items() if key not in selected]
    return {
        **recipe,
        'matched_ingredients': matches,
        'missing_ingredients': missing,
        'matching_ingredients': len(matches),
        'match_score': round(100 * len(matches) / len(ingredients)) if ingredients else 0,
    }
