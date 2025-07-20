from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from home.forms import SubscriberForm
from users.models import ContactInfo
from .utils import paginate_products
from cart.models import Order, OrderItem
from cart.utils import cookieCart
from django.db.models import Q



# Create your views here.

# @login_required()
def category(request):
    message = ''
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'تم الاشتراك بنجاح!'
            form = SubscriberForm()  # فرم جديد بعد الحفظ
    else:
        form = SubscriberForm()
    black_friday_deals = Product.objects.filter(
        black_friday_deal=True,
        available_at__lte=timezone.now()
    ).order_by('-available_at')
    contact = ContactInfo.objects.first()
    products = Product.objects.filter(
        available_at__lte=timezone.now()).order_by('-id')
    products_page = paginate_products(request, products, per_page=6)
    categories = Category.objects.all()
    categories_with_count = Category.objects.annotate(
        product_count=Count('products'))
    context = {
        'products_page': products_page,
        'categories': categories,
        'form': form,
        'message': message,
        'contact': contact,
        'black_friday_deals': black_friday_deals,
        'categories_with_count': categories_with_count
        
    }
    return render(request, 'category.html', context)

# @login_required()


def category_detail(request, slug):
    # search = request.GET.get('search')
    category = get_object_or_404(Category, slug=slug)
    
    message = ''
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'تم الاشتراك بنجاح!'
            form = SubscriberForm()  # فرم جديد بعد الحفظ
    else:
        form = SubscriberForm()
    black_friday_deals = Product.objects.filter(
        black_friday_deal=True,
        available_at__lte=timezone.now()
    ).order_by('-available_at')
    # if search:
    #     products = Product.objects.filter(
    #         Q(name__icontains=search) | Q(category__name__icontains=search),
    #         category=category
    #     ).order_by('-created_at')
    # else:
    #     products = Product.objects.filter(
    #         category=category).order_by('-created_at')
    products = Product.objects.filter(
        category=category).order_by('-created_at')
    products_page = paginate_products(request, products, per_page=5)
    

    contact = ContactInfo.objects.first()
    categories_with_count = Category.objects.annotate(
        product_count=Count('products'))

    return render(request, 'category_detail.html', {
        # 'search': search,

        'category': category,
        
        'form': form,
        'message': message,
        'black_friday_deals': black_friday_deals,
        'products': products,
        'products_page': products_page,
        'contact': contact,
        'categories_with_count': categories_with_count
    })


def single_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    # عرض الألوان والمقاسات المتاحة
    color_variations = product.variations.filter(
        variation_category='color', is_active=True)
    size_variations = product.variations.filter(
        variation_category='size', is_active=True)

    # نحاول نجيب اللون والمقاس من باراميتر الـ GET (لو اتبعتوا من الصفحة)
    selected_color = request.GET.get('color')
    selected_size = request.GET.get('size')

    quantity = 0

    if request.user.is_authenticated:
        order = Order.objects.filter(
            customer=request.user, complete=False).first()
        if order:
            # لو في لون ومقاس، نفلتر بيهم
            if selected_color and selected_size:
                order_item = OrderItem.objects.filter(
                    order=order,
                    product=product,
                    color=selected_color,
                    size=selected_size
                ).first()
                if order_item:
                    quantity = order_item.quantity
            else:
                # لو مفيش لون ومقاس، نجمع كل الكميات لنفس المنتج
                order_items = OrderItem.objects.filter(
                    order=order, product=product)
                quantity = sum([item.quantity for item in order_items])
    else:
        cookie_data = cookieCart(request)
        if selected_color and selected_size:
            for item in cookie_data['items']:
                if (item['product']['id'] == product.id and
                    item.get('color') == selected_color and
                        item.get('size') == selected_size):
                    quantity = item['quantity']
                    break
        else:
            # لو مفيش لون ومقاس، نجمع كل الكميات
            quantity = sum([
                item['quantity'] for item in cookie_data['items']
                if item['product']['id'] == product.id
            ])

    black_friday_deals = Product.objects.filter(
        black_friday_deal=True,
        available_at__lte=timezone.now()
    ).order_by('-available_at')

    comments = product.comments.all()
    reviews = product.reviews.all()
    comment_form = CommentForm()
    review_form = ReviewForm()

    return render(request, 'single-product.html', {
        'product': product,
        'color': color_variations,
        'size': size_variations,
        'quantity': quantity,
        'selected_color': selected_color,
        'selected_size': selected_size,
        'comments': comments,
        'reviews': reviews,
        'form': comment_form,
        'reviews_form': review_form,
        'black_friday_deals': black_friday_deals
    })
# @login_required()
def save_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form= CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()
            return redirect('single-product', pk=product.id)
        else:
            comments = product.comments.all()
        return render(request, 'single-product.html', {'product': product, 'form': form, 'comments': comments})
# @login_required()
def save_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        reviews_form = ReviewForm(request.POST)
        if reviews_form.is_valid():
            review = reviews_form.save(commit=False)
            review.product = product
            if request.user.is_authenticated:
                review.user = request.user
            review.save()
            return redirect('single-product', pk=product.id)
        else:
            reviews = product.reviews.all()
            return render(request, 'single-product.html', {'product': product, 'reviews_form': reviews_form, 'reviews': reviews})



