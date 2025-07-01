from django.shortcuts import render, get_object_or_404
from .models import Size, Category, ClothingItem


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = ClothingItem.objects.filter(available=True)

    category = None
    if category_slug:
        category = get_object_or_404(Category, category_slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'main/product/list.html',
                    {'category': category,
                     'categories': categories,
                     'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(ClothingItem, id=id, slug=slug, available=True)
    #похожие продукты на те, на стрканицу которых вы зашли
    related_products = ClothingItem.objects.filter(category=product.category,
                                                   available=True).exclude(id=product.id)[:4]
    return render(request, 'main/product/detail.html', {'product':product,
                                                        'related_products':related_products})
