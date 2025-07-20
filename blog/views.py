from django.shortcuts import get_object_or_404, render,redirect
from .models import Blog,Category,Comments
from users.models import ContactInfo
from django.contrib.auth import get_user_model
from home.forms import SubscriberForm
from products.utils import paginate_products
from django.db.models import Count
from .forms import CommentForm
from users.models import Profile
from django.db.models import Q

# Create your views here.

def blog(request):


    search = request.GET.get('search')
    if search:
        blogs = Blog.objects.filter(
            Q(title__icontains=search) | Q(category__name__icontains=search) | Q(content__icontains=search)
            ).order_by('-created_at')
    else:
        blogs = Blog.objects.all().order_by('-created_at')
    message = ''
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'تم الاشتراك بنجاح!'
            form = SubscriberForm()  # فرم جديد بعد الحفظ
    else:
        form = SubscriberForm()
    User = get_user_model()
    admin_user = User.objects.filter(is_superuser=True).first()
    # عملناها كومنت عشان البحث
    # blogs=Blog.objects.all()
    popular_blogs = Blog.objects.order_by('-views')[:3]
    blog_page = paginate_products(request, blogs, per_page=5)
    contact= ContactInfo.objects.first()
    # الحصول على عدد المدونات في كل فئة
    categories_with_count = Category.objects.annotate(
        blog_count=Count('posts'))
    first_three_without_count = categories_with_count[:3]

    return render(request, 'blog.html', {'admin_user': admin_user, 'blogs': blogs,'search':search, 'categories': first_three_without_count, 'categories_with_count': categories_with_count, 'contact': contact, 'form': form, 'message': message, 'blog_page': blog_page, 'popular_blogs': popular_blogs})

def single_blog(request,pk):
    blog = get_object_or_404(Blog, id=pk)
    message = ''
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'تم الاشتراك بنجاح!'
            form = SubscriberForm()  # فرم جديد بعد الحفظ
    else:
        form = SubscriberForm()
    form_comment = CommentForm()
    comments = blog.comments.all()
    User = get_user_model()
    
    admin_user = User.objects.filter(is_superuser=True).first()
    
    popular_blogs = Blog.objects.order_by('-views')[:3]
    prev_post = Blog.objects.filter(created_at__lt=blog.created_at).order_by('-created_at').first()
    next_post = Blog.objects.filter(created_at__gt=blog.created_at).order_by('created_at').first()  

    blog.views += 1
    blog.save(update_fields=['views'])
    contact = ContactInfo.objects.first()
    # الحصول على عدد المدونات في كل فئة
    categories_with_count = Category.objects.annotate(
        blog_count=Count('posts'))
    first_three_without_count = categories_with_count[:3]
    return render(request, 'single-blog.html', {'admin_user': admin_user, 'blog': blog, 'contact': contact, 'form': form, 'form_comment': form_comment, 'comments': comments, 'message': message, 'popular_blogs': popular_blogs, 'prev_post': prev_post, 'next_post': next_post, 'categories': first_three_without_count, 'categories_with_count': categories_with_count})


def category_detail(request, slug):
    search = request.GET.get('search')
    category = get_object_or_404(Category, slug=slug)
    if search:
        posts = Blog.objects.filter(
            Q(title__icontains=search) | Q(category__name__icontains=search),
            category=category
        ).order_by('-created_at')
    else:
        posts = Blog.objects.filter(category=category).order_by('-created_at')

    message = ''
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'تم الاشتراك بنجاح!'
            form = SubscriberForm()  # فرم جديد بعد الحفظ
    else:
        form = SubscriberForm()
    User = get_user_model()
    admin_user = User.objects.filter(is_superuser=True).first()
    #عملناها كومنت عشان البحث
    # posts = Blog.objects.filter(category=category)
    blog_page = paginate_products(request, posts, per_page=5)
    popular_blogs = Blog.objects.order_by('-views')[:3]
    contact = ContactInfo.objects.first()
    # الحصول على عدد المدونات في كل فئة
    categories_with_count = Category.objects.annotate(
        blog_count=Count('posts'))
    first_three_without_count = categories_with_count[:3]
    return render(request, 'category-detail.html', {'admin_user': admin_user,'search':search, 'category': category, 'posts': posts, 'blog_page': blog_page, 'contact': contact, 'form': form, 'message': message, 'popular_blogs': popular_blogs, 'categories': first_three_without_count, 'categories_with_count': categories_with_count})


def save_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    # إضافة admin_user
    User = get_user_model()
    admin_user = User.objects.filter(is_superuser=True).first()

    if request.method == 'POST':
        form_comment = CommentForm(request.POST)
        if form_comment.is_valid():
            comment = form_comment.save(commit=False)
            comment.blog = blog
            if request.user.is_authenticated:
                comment.user = request.user
            # معالجة الرد على تعليق
            parent_id = request.POST.get('parent')
            if parent_id:
                try:
                    parent_comment = Comments.objects.get(id=parent_id)
                    comment.parent = parent_comment
                except Comments.DoesNotExist:
                    pass  # تجاهل لو parent مش موجود

            comment.save()
            return redirect('single-blog', pk=blog.id)
        else:
            # releated_name #لو حصل خطأ بيرجع نفس الصفحه بالتعليقات القديمه
            comments = blog.comments.all()
            return render(request, 'single-blog.html', {'blog': blog, 'form_comment': form_comment, 'comments': comments, 'admin_user': admin_user})
