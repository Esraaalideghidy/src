from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,get_object_or_404,redirect
from .models import Order, OrderItem, ShippingAddress
from django.http import JsonResponse
import json
from home.forms import SubscriberForm
from users.models import ContactInfo
from products.models import Product
import datetime
from .utils import cookieCart, cartData, guestOrder
from users.models import User
# Create your views here.

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']


    context = {
        'items': items, 
        'order': order,
        'cartItems': cartItems,
    }

    return render(request, 'cart.html', context)

def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']



    context = {
        'items': items,
        'order': order,
        'shipping': False,
        'cartItems': cartItems
    }
    return render(request, 'checkout.html',context)






def updateItem(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    try:
        quantity = int(data.get('quantity', 1))
    except ValueError:
        quantity = 1

    selected_color = data.get('color') or None
    selected_size = data.get('size') or None

    user = request.user
    product = Product.objects.get(id=productId)
    order = Order.objects.filter(customer=user, complete=False).first()

    if not order:
        if action == 'add':
            order = Order.objects.create(customer=user, complete=False)
        else:
            return JsonResponse({'message': 'No active order to update'}, safe=False)

    filters = {
        'order': order,
        'product': product,
        'color__isnull': selected_color is None,
        'size__isnull': selected_size is None,
    }

    if selected_color is not None:
        filters['color'] = selected_color
        filters.pop('color__isnull', None)

    if selected_size is not None:
        filters['size'] = selected_size
        filters.pop('size__isnull', None)

    orderItems = OrderItem.objects.filter(**filters)

    # لو المستخدم ضغط "delete"
    if action == 'delete':
        deleted_count, _ = orderItems.delete()
        return JsonResponse({'message': f'{deleted_count} item(s) deleted'}, safe=False)

    # لو "add" أو "remove"
    if orderItems.exists():
        orderItem = orderItems.first()
    else:
        orderItem = OrderItem.objects.create(
            order=order,
            product=product,
            color=selected_color,
            size=selected_size,
            quantity=0
        )

    if action == 'add':
        orderItem.quantity += quantity
    elif action == 'remove':
        orderItem.quantity -= quantity

    if orderItem.quantity <= 0:
        orderItem.delete()
    else:
        orderItem.save()

    return JsonResponse({'message': 'Item was updated'}, safe=False)

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = request.user
        # order, created = Order.objects.get_or_create(
        #     customer=user, complete=False)
        order = Order.objects.filter(customer=user, complete=False).first()

        if not order:
            return JsonResponse({'error': 'No active order found'}, status=400)

    else:
        user, order = guestOrder(request, data)

    # التحقق من السعر
    try:
        total = Decimal(str(data['form']['total']))
    except:
        return JsonResponse({'error': 'Invalid total'}, status=400)
    shipping = Decimal('50')
    expected_total = Decimal(order.get_cart_total())+shipping   

    print("🔢 Client total:", total)
    print("🔢 Expected total:", expected_total)

    order.transaction_id = transaction_id

    if abs(total) - abs(expected_total) < Decimal('0.01'):
        order.complete = True
        print("✅ Order marked as complete.")
    else:
        print("❌ Totals do not match! Order not marked as complete.")
    order.save()

        # عنوان الشحن (لو الطلب يحتاج شحن)
    if order.shipping:
            ShippingAddress.objects.create(
                customer=user,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

        # ✅ ربط الطلب بحساب المستخدم الحقيقي في حالة تسجيل الدخول بعد الدفع
    # نحاول نربط الطلب بالمستخدم الجديد بعد تسجيل الدخول
    guest_id = request.session.get('guest_id')

    if guest_id and request.user.is_authenticated:
        guest_user = User.objects.filter(id=guest_id).first()

        # تأكد إن الضيف موجود ومختلف عن المستخدم الحالي
        if guest_user and guest_user != request.user:
            # تحديث الطلبات القديمة وربطها بالمستخدم الحالي
            orders = Order.objects.filter(customer=guest_user)
            for order in orders:
                order.customer = request.user
                order.save()

            # حذف الحساب الضيف لو ملوش باسورد (يعني مؤقت)
            if not guest_user.has_usable_password():
                guest_user.delete()

            # إزالة guest_id من السيشن
            del request.session['guest_id']


    return JsonResponse({'message':'Payment submitted..', 'transaction_id': transaction_id }, safe=False)


def confirmation(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'تم الاشتراك بنجاح!'
            form = SubscriberForm()  # فرم جديد بعد الحفظ
    else:
        form = SubscriberForm()
    contact = ContactInfo.objects.first()

    transaction_id = request.GET.get('transaction_id')
    order = None
    items = []
    shipping_address = None

    # 1. هل المستخدم الحالي هو زائر وسبق حفظ له طلب؟
    guest_id = request.session.get('guest_id')
    if guest_id:
        guest_user = User.objects.filter(id=guest_id).first()
        if guest_user:
            # لو المستخدم سجل دلوقتي، انقل الطلب
            if request.user.is_authenticated and guest_user != request.user:
                Order.objects.filter(customer=guest_user).update(
                    customer=request.user)
                if not guest_user.has_usable_password():
                    guest_user.delete()
                del request.session['guest_id']

    # 2. دلوقتي هنعمل محاولة جلب الطلب النهائي
    if request.user.is_authenticated:
        order = Order.objects.filter(
            customer=request.user, complete=True).last()
    elif guest_id:
        guest_user = User.objects.filter(id=guest_id).first()
        if guest_user:
            order = Order.objects.filter(
                customer=guest_user, complete=True).last()

    # 3. لو مفيش طلب، ارجع بخطأ
    if not order:
        return render(request, 'confirmation.html', {'error': 'Order not found.'})

    # 4. جبنا الطلب بنجاح
    items = order.orderitem_set.all()
    shipping_address = ShippingAddress.objects.filter(order=order).last()

    context = {
        'order': order,
        'items': items,
        'shipping_address': shipping_address,
        'form': form,
    }
    return render(request, 'confirmation.html', context)
