from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY = (
    ('Normal', 'Normal'),
    ('Fire', 'Fire'),
    ('Water', 'Water'),
    ('Grass', 'Grass'),
    ('Electric', 'Electric'),
    ('Ice', 'Ice'),
    ('Fighting', 'Fighting'),
    ('Poison', 'Poison'),
    ('Ground', 'Ground'),
    ('Flying', 'Flying'),
    ('Psychic', 'Psychic'),
    ('Bug', 'Bug'),
    ('Rock', 'Rock'),
    ('Ghost', 'Ghost'),
    ('Dark', 'Dark'),
    ('Dragon', 'Dragon'),
    ('Steel', 'Steel'),
    ('Fairy', 'Fairy'),
)
class Category(models.Model):
    name = models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.ManyToManyField(Category)
    quantity = models.PositiveIntegerField(null=True)
    image = models.ImageField(upload_to='media')

    class Meta:
        verbose_name_plural = 'Product'

    def __str__(self):
        return f'{self.name}'
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category)

    class Meta:
        verbose_name_plural = 'Order'

    def __str__(self):
        return f'{self.product} - ordered ({self.order_quantity}) by {self.staff}'
 
