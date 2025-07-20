from django.db import models
import uuid
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
# from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    img= models.ImageField(upload_to='category/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True)


    def __str__(self):
        return self.name

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    img = models.ImageField(upload_to='product/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    available_at = models.DateTimeField(default=timezone.now)
    width= models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    height= models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    length= models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    weight= models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Depth= models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Quality_checking= models.BooleanField(default=False)
    Freshness_Duration= models.IntegerField(null=True, blank=True)  # in days
    When_packeting= models.DateTimeField(null=True, blank=True)
    Each_Box_contains= models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0)
    is_hot_deal = models.BooleanField(default=False)
    hot_deal_end_at = models.DateTimeField(null=True, blank=True)
    black_friday_deal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,null=True, on_delete=models.CASCADE, related_name='products', default=None, blank=True)
    digital = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
    @property
    def in_stock(self):
        return self.stock > 0

    def get_absolute_url(self):
        return reverse('single-product', kwargs={'pk': self.pk})

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color', is_active=True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size', is_active=True)
variation_category_choices=(
    ('color', 'color'),
    ('size', 'size'),
)

class variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    variation_category=models.CharField(max_length=100, choices=variation_category_choices)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    

    def __unicode__(self):
        return self.product
class Comment(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    phone_number= models.CharField(max_length=15, null=True, blank=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.name}'
    
class Reviews(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    review = models.TextField()
    phone_number= models.CharField(max_length=15, null=True, blank=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'review by {self.name}'
