# urls.py
from django.urls import path
from . import views

app_name = "Apps.compras"
urlpatterns = [
    path('', views.sales_list_view, name='compras'),
    path('realizar_compra/', views.show_realizar_compra, name='realizar_compra'),
    path('realizar_compra/submit/', views.realizar_compra, name='realizar_compra_submit'),
]
