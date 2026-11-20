from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models


DAYS_OF_THE_WEEK = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electronico')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=225, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class Meal(models.Model):
    meal_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='meals',
    )

    def __str__(self):
        return self.name


class MealPlan(models.Model):
    meal_plan_id = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='meal_plans',
    )
    client_name = models.CharField(max_length=100)
    client_weight = models.FloatField()
    client_height = models.FloatField()
    plan_type = models.CharField(max_length=100)
    plan_length_in_weeks = models.PositiveIntegerField()
    current_week = models.PositiveIntegerField()
    tracking_days = models.JSONField(default=list, blank=True)
    prep_day = models.CharField(choices=DAYS_OF_THE_WEEK, max_length=20)
    daily_goals = models.JSONField(default=dict, blank=True)
    meals_per_day = models.JSONField(default=dict, blank=True)
    meals = models.JSONField(default=dict, blank=True)

    def clean(self):
        super().clean()
        if self.client_weight <= 0:
            raise ValidationError({'client_weight': 'Debe ser mayor que cero.'})
        if self.client_height <= 0:
            raise ValidationError({'client_height': 'Debe ser mayor que cero.'})
        if self.plan_length_in_weeks < 1:
            raise ValidationError({
                'plan_length_in_weeks': 'Debe ser al menos una semana.'
            })
        if self.current_week < 1:
            raise ValidationError({
                'current_week': 'Debe ser al menos la semana uno.'
            })
        if self.current_week > self.plan_length_in_weeks:
            raise ValidationError({
                'current_week': 'No puede superar la duración del plan.'
            })
        valid_days = {day[0] for day in DAYS_OF_THE_WEEK}
        if not isinstance(self.tracking_days, list):
            raise ValidationError({
                'tracking_days': 'Debe ser una lista de días.'
            })
        invalid_days = set(self.tracking_days) - valid_days
        if invalid_days:
            raise ValidationError({
                'tracking_days': 'Contiene días no válidos.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.meal_plan_id} - {self.client_name}'


class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    meal_id = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    image_url = models.URLField()
    isMealPrepRecipe = models.BooleanField(default=False)
    time_minutes = models.PositiveIntegerField()
    price_level = models.PositiveIntegerField()
    tags = models.ManyToManyField('Tag', related_name='recipes')
    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name='recipes',
    )
    instructions = models.TextField()
    nutritionalInfo = models.JSONField(default=dict)

    def clean(self):
        super().clean()
        if self.time_minutes < 1:
            raise ValidationError({
                'time_minutes': 'Debe ser al menos un minuto.'
            })
        if not 1 <= self.price_level <= 5:
            raise ValidationError({
                'price_level': 'Debe estar entre 1 y 5.'
            })

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tags',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique_tag_per_user',
            )
        ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    label = models.CharField(max_length=255)
    amount = models.CharField(max_length=10)
    unit = models.CharField(max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ingredients',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'label', 'amount', 'unit'],
                name='unique_ingredient_per_user',
            )
        ]

    def __str__(self):
        return self.label
