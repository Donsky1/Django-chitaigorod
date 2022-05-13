from django.db import models
from django.core.files.images import get_image_dimensions
from PIL import Image
from django.core.exceptions import ValidationError


# Create your models here.
class CommonInfo(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Category(CommonInfo):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(CommonInfo):

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Complexity(CommonInfo):

    class Meta:
        verbose_name = 'Уровень сложности приготовления'
        verbose_name_plural = 'Уровни сложности приготовления'


def validate_image(image_obj):
    file_size = image_obj.file.size
    megabyte_limit = 1.0
    if file_size > megabyte_limit*1024*1024:
        raise ValidationError('Размер вашей картинки %s мб. Максимальный размер картинки %s мб' %
                              (round(file_size/1024/1024, 2), megabyte_limit))


class Dishes(models.Model):
    title = models.CharField(max_length=64, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    complexity = models.ForeignKey(Complexity, on_delete=models.CASCADE)
    timeprocess = models.CharField(max_length=16, blank=True)
    calories = models.CharField(max_length=6, blank=True)
    rating = models.CharField(max_length=3, blank=True)
    image = models.ImageField(upload_to='images_small', null=True, blank=True,
                              validators=[validate_image],
                              help_text='Максимальный размер картинки 1 мб, резрешение 150х150')
    description = models.TextField()
    image_full = models.ImageField(upload_to='images_full', null=True, blank=True,
                                   validators=[validate_image],
                                   help_text='Максимальный размер картинки 1 мб')
    description_full = models.TextField(blank=True)
    nutrition = models.TextField(blank=True)
    ingredients_clr = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    link = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    @staticmethod
    def resize_image(set_h, set_w, image):
        h, w = get_image_dimensions(image.path)
        img = Image.open(image)
        if h > set_h or w > set_w:
            output_size = (set_h, set_w)
            img.thumbnail(output_size)
            img.save(image.path)

    def save(self, *args, **kwargs):
        super(Dishes, self).save(*args, **kwargs)
        if self.image:
            self.resize_image(150, 150, self.image)
        if self.image_full:
            self.resize_image(375, 500, self.image_full)

    def display_tags(self):
        tags = self.tags.all()
        return ', '.join([tag.name for tag in tags])