from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Complexity(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


class Dishes(models.Model):
    title = models.CharField(max_length=64, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)
    complexity = models.ForeignKey(Complexity, on_delete=models.PROTECT)
    timeprocess = models.CharField(max_length=16, blank=True)
    calories = models.CharField(max_length=6, blank=True)
    rating = models.CharField(max_length=3, blank=True)
    image = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title