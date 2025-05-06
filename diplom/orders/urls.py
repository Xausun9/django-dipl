from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.index, name='index'),
    path('task/new/', views.new_task, name='new_task'),
]