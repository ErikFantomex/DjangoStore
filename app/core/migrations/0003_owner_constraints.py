from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def assign_existing_records(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL.split('.')[0],
                          settings.AUTH_USER_MODEL.split('.')[1])
    first_user = User.objects.first()
    if not first_user:
        return
    for model_name in ('Meal', 'MealPlan'):
        Model = apps.get_model('core', model_name)
        Model.objects.filter(user__isnull=True).update(user=first_user)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_meal_mealplan'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='user',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='meals',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='user',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='meal_plans',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(assign_existing_records, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='meal',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='meals',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='mealplan',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='meal_plans',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='time_minutes',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='price_level',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='mealplan',
            name='plan_length_in_weeks',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='mealplan',
            name='current_week',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='mealplan',
            name='tracking_days',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='mealplan',
            name='daily_goals',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='mealplan',
            name='meals_per_day',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='mealplan',
            name='meals',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='nutritionalInfo',
            field=models.JSONField(default=dict),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(
                fields=('user', 'name'),
                name='unique_tag_per_user',
            ),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(
                fields=('user', 'label', 'amount', 'unit'),
                name='unique_ingredient_per_user',
            ),
        ),
    ]
