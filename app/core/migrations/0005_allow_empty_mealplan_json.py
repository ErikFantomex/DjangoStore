from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_alter_ingredient_user_alter_recipe_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealplan',
            name='tracking_days',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='mealplan',
            name='daily_goals',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='mealplan',
            name='meals_per_day',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='mealplan',
            name='meals',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
