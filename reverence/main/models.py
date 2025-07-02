from django.db import models
from django.urls import reverse
#reverse — это функция для генерации URL по имени маршрута (удобно, т.к. не "зашиваем" URL вручную) - строит URL на основе имени маршрута из urls.py

class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)


    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)


    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])] #создаем индекс в базе данных по полю name для более быстрого поиска
        verbose_name = 'category'
        verbose_name_plural = 'categories'

        def __str__(self):
            return self.name

    def get_absolute_url(self):
        return reverse('main:product_list_by_category', args=[self.slug])
#найти URL с именем product_list_by_category в пространстве имён main, и подставить туда self.slug

class ClothingItem(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    available = models.BooleanField(default=True)
    sizes = models.ManyToManyField(Size, through='ClothingItemSize', #through - имя связующей таблицы
                                   related_name='clothing_item', blank=True) #related_name - как обращаться к элементу
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='clothing_items')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('main:product_detail', args=[self.id, self.slug])


    def get_price_with_discount(self):
        if self.discount > 0:
            return self.price * (1 - (self.discount / 100))
        return self.price


class ClothingItemSize(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)


    class Meta:
        unique_together = ('clothing_item', 'size')