# products/utils.py

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate_products(request, queryset, per_page=6):
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page', 1)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)
