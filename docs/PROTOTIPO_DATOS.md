# Prototipo de ciencia de datos nutricionales

Este prototipo adapta **los archivos de este proyecto** (Django, Angular y PostgreSQL). El caso de uso es ayudar a un nutriólogo a comparar productos envasados mediante datos nutricionales por 100 g. El usuario elige un producto de un catálogo con fotos. Django usa su código de barras para consultar la API pública de [Open Food Facts](https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/) y guarda una copia en PostgreSQL. Angular muestra indicadores, gráficos y la tabla de registros.

## Arquitectura

```text
Navegador → Angular (frontend, puerto 4200)
                 ↓ /api
             Django (app, puerto 8000) → Open Food Facts (HTTPS)
                 ↓
             PostgreSQL (db, volumen persistente)
```

`docker-compose.yml` define **tres contenedores**. Django cumple la función de API e importador; Angular es la aplicación de visualización. Se conserva el resto del portal: recetas, planes, comidas, usuarios y autenticación. No se utilizan los archivos del proyecto de ejemplo `dash-mysql.zip`.

## Requisitos y arranque

- Docker Desktop con Docker Compose.
- Conexión a Internet para importar productos nuevos. Los productos ya guardados siguen visibles sin conexión.

En PowerShell, desde la raíz del proyecto:

```powershell
Copy-Item .env.example .env
```

Edita `.env` y cambia `OPEN_FOOD_FACTS_USER_AGENT` para poner tu correo de contacto real con el formato `PortalNutricional/1.0 (correo@dominio.com)`. Open Food Facts pide identificar la aplicación mediante ese encabezado. Después:

```powershell
docker compose up --build -d
docker compose ps
```

Abre <http://localhost:4200>, crea una cuenta en **Registro**, inicia sesión y entra a **Alimentos**. La primera compilación puede tardar varios minutos. Swagger está en <http://localhost:8000/api/docs/>.

## Demostración para clase

Guion breve para la exposición:

- **Necesidad:** comparar productos envasados sin copiar manualmente sus etiquetas nutricionales.
- **API:** Open Food Facts devuelve nombre, marca, energía, macronutrientes y Nutri-Score por código de barras.
- **Contenedores:** Angular presenta los gráficos; Django consulta la API externa y expone endpoints propios; PostgreSQL conserva los datos.
- **Base de datos:** una fila por código de barras, con valores por 100 g y fecha de actualización.
- **Flujo:** consultar → guardar → visualizar → recargar para comprobar persistencia.

1. Enseña que `docker compose ps` muestra `frontend`, `app` y `db` activos.
2. En **Alimentos**, filtra por **Legumbres**, selecciona un producto y pulsa **Agregar a la comparación**. La aplicación solicita datos a Open Food Facts y los guarda en la tabla `food_foodproduct`.
3. Elige otro producto del mismo grupo. Observa el total, los promedios, el gráfico de calorías, los macronutrientes y los registros.
4. Vuelve a seleccionar e importar el primer producto. Se actualiza el registro existente sin duplicarlo, gracias al campo `barcode` único.
5. Recarga la página para demostrar que los gráficos se alimentan de PostgreSQL, no de datos temporales del navegador.

Para comprobar el almacenamiento directamente:

```powershell
docker compose exec db psql -U devuser -d devdb -c "SELECT barcode, name, calories_100g, protein_100g, fetched_at FROM food_foodproduct ORDER BY name;"
```

Para comprobar la API sin depender del navegador, obtén un token con las credenciales de tu cuenta y consulta los productos:

```powershell
$token = (Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/user/token/ -ContentType 'application/json' -Body '{"email":"tu-correo@ejemplo.com","password":"tu-clave"}').token
Invoke-RestMethod -Uri http://localhost:8000/api/food/products/ -Headers @{Authorization="Token $token"}
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/food/products/import/ -Headers @{Authorization="Token $token"} -ContentType 'application/json' -Body '{"barcode":"3017620422003"}'
Invoke-RestMethod -Uri http://localhost:8000/api/food/summary/ -Headers @{Authorization="Token $token"}
```

## Diseño de datos

La migración `food/migrations/0001_initial.py` crea `food_foodproduct`:

| Campo | Función |
| --- | --- |
| `barcode` | Código de barras único; evita duplicados. |
| `name`, `brand` | Nombre y marca devueltos por la API. |
| `image_url` | Foto del empaque en Open Food Facts, si está disponible. |
| `calories_100g`, `protein_100g`, `carbohydrates_100g`, `fat_100g`, `sugars_100g` | Valores numéricos por 100 g; pueden ser nulos cuando faltan en la fuente. |
| `nutriscore` | Clasificación A–E, si existe. |
| `fetched_at` | Fecha y hora de la última importación. |

La lista y los promedios se calculan sobre registros de PostgreSQL. El navegador filtra un catálogo local de 118 productos en nueve categorías. Al agregar un alimento a la comparación, Django consulta sus valores actuales en Open Food Facts. Las rutas `/api/food/products/`, `/api/food/products/import/` y `/api/food/summary/` requieren token de usuario.

El archivo [product-catalog.ts](../frontend/src/app/pages/food-data/product-catalog.ts) contiene una selección de datos derivados de Open Food Facts bajo ODbL. Las fotos enlazadas mantienen la licencia CC BY-SA de la fuente. [Licencias de Open Food Facts](https://openfoodfacts.github.io/openfoodfacts-server/api/).

## Pruebas y cierre

```powershell
docker compose exec app python manage.py test food
docker compose down
```

El volumen `dev-db-data` conserva los datos entre arranques. `docker compose down -v` elimina ese volumen y reinicia los registros de la demostración.

**Fuente y alcance:** [Open Food Facts](https://world.openfoodfacts.org/) ofrece datos colaborativos; algunas cifras pueden faltar o cambiar. La API limita las consultas de productos a 15 por minuto por IP según su [documentación](https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/). Este prototipo es una herramienta de comparación, no una fuente clínica de referencia.
