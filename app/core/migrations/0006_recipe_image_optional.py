from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('core', '0005_allow_empty_mealplan_json')]
    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]
