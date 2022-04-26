from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Complexity(models.Model):
    name = models.CharField(max_length=16, unique=True)

    class Meta:
        verbose_name = 'Уровень сложности приготовления'
        verbose_name_plural = 'Уровни сложности приготовления'

    def __str__(self):
        return self.name


class Dishes(models.Model):
    title = models.CharField(max_length=64, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    complexity = models.ForeignKey(Complexity, on_delete=models.CASCADE)
    timeprocess = models.CharField(max_length=16, blank=True)
    calories = models.CharField(max_length=6, blank=True)
    rating = models.CharField(max_length=3, blank=True)
    image = models.ImageField(upload_to='images_small', null=True, blank=True)
    description = models.TextField()
    image_full = models.ImageField(upload_to='images_full', null=True, blank=True)
    description_full = models.TextField(blank=True)
    nutrition = models.TextField(blank=True)
    ingredients_clr = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    link = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.title