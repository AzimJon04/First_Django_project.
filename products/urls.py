from django.urls import path
from .views import ProductsList, CategoriesList
from .views import products_detail, products_by_category, ProductsCreate, ProductsUpdate, ProductsDelete
from .views import add_to_basket, baskets_detail, baskets_remove
from .views import add_to_order, orders_detail

urlpatterns = [
    path('', ProductsList.as_view(), name='home'),
    path('basket/', baskets_detail, name='basket'),
    path('add_to_basket/<int:id_product>/', add_to_basket, name='add_to_basket'),
    path('basket_remove/<int:id_basket>/', baskets_remove, name='basket_remove'),
    path('order/<int:id_basket>/', add_to_order, name='add_to_order'),
    path('orders/', orders_detail, name='orders'),
    path('categories/', CategoriesList.as_view(), name='categories'),
    path('products/<int:id_product>/', products_detail, name='products_detail'),
    path('category/<int:category_id>/', products_by_category, name='products_by_category'),
    path('create/', ProductsCreate.as_view(), name='create_product'),
    path('products/<int:pk>/update', ProductsUpdate.as_view(), name='update_product'),
    path('products/<int:pk>/delete', ProductsDelete.as_view(), name='delete_product'),
]
