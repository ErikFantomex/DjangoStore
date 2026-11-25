from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='FoodProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barcode', models.CharField(max_length=14, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('brand', models.CharField(blank=True, max_length=255)),
                ('calories_100g', models.FloatField(blank=True, null=True)),
                ('protein_100g', models.FloatField(blank=True, null=True)),
                ('carbohydrates_100g', models.FloatField(blank=True, null=True)),
                ('fat_100g', models.FloatField(blank=True, null=True)),
                ('sugars_100g', models.FloatField(blank=True, null=True)),
                ('nutriscore', models.CharField(blank=True, max_length=1)),
                ('fetched_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['name', 'barcode']},
        ),
    ]
