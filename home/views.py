from django.core.paginator import Paginator
from .forms import SubscriberForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product, Category
from products.utils import paginate_products
from django.utils import timezone
from .forms import SubscriberForm
from users.models import ContactInfo
from django.db.models import Q, Count
# Create your views here.

def home(request):
    #subscriber in footer
    message = ''
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'تم الاشتراك بنجاح!'
            form = SubscriberForm()  # فرم جديد بعد الحفظ
    else:
        form = SubscriberForm()

    #show the social media in users.models
    contact = ContactInfo.objects.first()
    #show product in products.models
    products = Product.objects.filter(
        available_at__lte=timezone.now()
    ).order_by('-available_at')
    products_page = paginate_products(request, products, per_page=8)
    future_products = Product.objects.filter(
        available_at__gt=timezone.now()
    ).order_by('available_at')
    hot_deals = Product.objects.filter(
        is_hot_deal=True,
        available_at__lte=timezone.now()
    ).order_by('-available_at')
    if hot_deals.exists():
        deal_end = hot_deals.first().hot_deal_end_at
        if deal_end < timezone.now():
            deal_end = None
        
    else:
        deal_end = None
    
    black_friday_deals = Product.objects.filter(
        black_friday_deal=True,
        available_at__lte=timezone.now()
    ).order_by('-available_at')
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'form': form,
        'message': message,
        'contact': contact,
        'products_page': products_page,
        'categories': categories,
        'future_products': future_products,
        'hot_deals': hot_deals,
        'deal_end': deal_end,
        'black_friday_deals': black_friday_deals,

   

    })


def search(request):
    message = ''
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'تم الاشتراك بنجاح!'
            form = SubscriberForm()  # فرم جديد بعد الحفظ
    else:
        form = SubscriberForm()

    contact = ContactInfo.objects.first()

    keyword = request.GET.get('keyword', '')
    categories_with_count = Category.objects.annotate(
        product_count=Count('products'))
    products = Product.objects.none()  # مبدئياً فاضي

    if keyword:
        products = Product.objects.filter(
            Q(name__icontains=keyword) |
            Q(description__icontains=keyword)
        )

    # ✅ Pagination
    paginator = Paginator(products, 6)  # 6 منتجات في الصفحة
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    context = {
        'keyword': keyword,
        'categories_with_count': categories_with_count,
        'products_page': products_page,
        'message': message,
        'form': form,
        'contact': contact,

    }

    return render(request, 'category.html', context)
