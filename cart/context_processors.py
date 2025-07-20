from .models import Order
from .utils import cookieCart, cartData

def cart_items_count(request):
    cartItems = 0
    if request.user.is_authenticated:
        order = Order.objects.filter(
            customer=request.user, complete=False).first()
        if order:
            # بيعد عدد العناصر اللي موجود مع كل زياده ف العنصر من العدد يعني
            cartItems = order.get_cart_items
        # cartItems = order.orderitem_set.count()   #بيعد عدد العناصر الفعليه
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    
    return {'cartItems': cartItems}
