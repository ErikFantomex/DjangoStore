from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('food', '0001_initial')]

    operations = [
        migrations.AddField(
            model_name='foodproduct',
            name='image_url',
            field=models.URLField(blank=True, max_length=500),
        ),
    ]
