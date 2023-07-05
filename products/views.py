from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from .models import Categories, Products, Basket, Orders
from .forms import ProductsForm
from django.contrib.auth.decorators import login_required


# Create your views here.

class CategoriesList(ListView):
    model = Categories
    template_name = 'products/category_list.html'
    context_object_name = 'categories'


class ProductsList(ListView):
    model = Products
    template_name = 'products/home.html'
    context_object_name = 'products'


def products_detail(request, id_product):
    product = Products.objects.get(id=id_product)
    return render(request, 'products/products_detail.html', {'product': product})


def products_by_category(request, category_id):
    products = Products.objects.filter(categories=category_id)
    category = Categories.objects.get(pk=category_id)
    context = {'products': products, 'category': category}
    return render(request, 'products/products_by_category.html', context)


class ProductsCreate(CreateView):
    model = Products
    form_class = ProductsForm
    template_name = 'products/products_create.html'
    success_url = reverse_lazy('home')


class ProductsUpdate(UpdateView):
    model = Products
    fields = ['name', 'author', 'description', 'price', 'categories']
    template_name = 'products/products_update.html'
    success_url = reverse_lazy('home')


class ProductsDelete(DeleteView):
    model = Products
    template_name = 'products/products_delete.html'
    success_url = reverse_lazy('home')


@login_required
def add_to_basket(request, id_product):
    product = Products.objects.get(id=id_product)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        baskets = baskets.first()
        baskets.quantity += 1
        baskets.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required()
def baskets_detail(request):
    baskets = Basket.objects.filter(user=request.user)
    return render(request, 'products/baskets_detail.html', {'baskets': baskets})


@login_required
def baskets_remove(request, id_basket):
    basket = Basket.objects.get(id=id_basket)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def add_to_order(request, id_basket):
    basket = Basket.objects.get(id=id_basket)
    order = Orders.objects.filter(user=request.user, product=basket.product)

    if not order.exists():
        Orders.objects.create(user=request.user, product=basket.product, quantity=basket.quantity)
        basket.delete()
    else:
        order = order.first()
        order.quantity += basket.quantity
        order.save()
        basket.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def orders_detail(request):
    orders = Orders.objects.filter(user=request.user)
    return render(request, 'products/orders_detail.html', {'orders': orders})
