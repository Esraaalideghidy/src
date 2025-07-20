from django.db import models
from users.models import User
from products.models import Product

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.username if self.customer else 'Guest'}"
    

    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.get_total() for item in orderitems)
        return total
    
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total_items = sum(item.quantity for item in orderitems)
        return total_items 
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if item.product.digital == False:
                shipping = True
        return shipping
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        product_name = self.product.name if self.product else "Deleted Product"
        order_id = self.order.id if self.order else "No Order"
        return f"{product_name} (Order {order_id})"
    

    def get_total(self):
        total= self.product.price * self.quantity
        return total
    
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        order_info = f"Order {self.order.id}" if self.order else "No Order"
        customer_info = self.customer.username if self.customer else "No Customer"
        return f"Shipping Address for {order_info} by {customer_info}"
