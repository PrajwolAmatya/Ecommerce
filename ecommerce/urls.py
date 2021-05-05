from django.urls import path
from .views import *

app_name = 'ecommerce'  # namespace

urlpatterns = [
    path('', Homepage.as_view(), name='index'),
    path('register', SignUpView.as_view(), name='register'),

    path('category/<str:category_slug>', CategoryWise.as_view(), name='category_wise'),
    path('product/<str:product_slug>', ProductView.as_view(), name='single_product'),
    path('search/', SearchView.as_view(), name='search'),

    path('api/categories', CategoryApiView.as_view()),
    path('cart', CartView.as_view(), name='cart'),

    path('close-add', CloseAdView.as_view(), name='close_ad'),  # url ma chai hyphen - not _

]
