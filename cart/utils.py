import json
# from cart.views import *
from products.models import Product
from cart.models import Order, OrderItem
from django.utils.crypto import get_random_string
from users.models import User


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES.get('cart'))
        print("🧩 Raw cart from cookies:", request.COOKIES.get('cart'))
    except:
        cart = {}
        print('Cart is empty or broken')

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}

    for i in cart:
        try:
            quantity = cart[i]['quantity']
            selected_color = cart[i].get('color', None)
            selected_size = cart[i].get('size', None)
            product = Product.objects.get(id=i)
            total = product.price * quantity
            order['get_cart_total'] += total
            order['get_cart_items'] += quantity

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'img': product.img.url if getattr(product.img, 'url', None) else '/static/blog/c2.jpg',
                },
                'quantity': quantity,
                'get_total': total,
                'color': selected_color,
                'size': selected_size,
            }
            items.append(item)

            if not product.digital:
                order['shipping'] = True
        except:
            pass

    cartItems = order['get_cart_items']

    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    if request.user.is_authenticated:
        # Here you can fetch the user's cart items if needed
        user = request.user
        order = Order.objects.filter(customer=user, complete=False).first()

        # 🛑 هنا نمنع إنشاء order فاضي
        if not order or not order.orderitem_set.exists():
            return {
                'items': [],
                'order': {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False},
                'cartItems': 0
            }
        # items = order.orderitem_set.all()
        # items = order.orderitem_set.all()
        # # if hasattr(order, 'get_cart_items'):
        # #     cartItems = order.get_cart_items
        # # else:
        # #     cartItems = 0
        # cartItems = order.get_cart_items
        # استبعد العناصر اللي المنتج بتاعها اتحذف
        items = []
        for item in order.orderitem_set.all():
            if item.product is not None:
                items.append(item)
            else:
                item.delete()  # امسحي العنصر لو المنتج المرتبط اتحذف

        cartItems = sum([item.quantity for item in items])

        

    else:
        cookieData=cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']



    return{
        'items': items,
        'order': order,
        'cartItems': cartItems  
    }    



def guestOrder(request, data):

    name = data['form']['name']
    email = data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']
    
    #توليد يوزر نيم فريد من نوعه
    try:
        user = User.objects.get(email=email)
        created = False
    except User.DoesNotExist:
       
        user = User.objects.create(
            username=name,
            first_name=name,
            email=email,
        )
        user.set_unusable_password()
        user.save()
        created = True
    request.session['guest_id'] = user.id
    order = Order.objects.create(
                customer=user,
                complete=False,
            )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
            color=item.get('color'),
            size=item.get('size'),
        )

    return user, order   