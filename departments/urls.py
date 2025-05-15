from django.urls import path
from . import views

urlpatterns = [
    path('', views.department_list, name='department_list'),
    path('create/', views.create_department, name='create_department'),
    path('update/<int:pk>/', views.update_department, name='update_department'),
    path('delete/<int:pk>/', views.delete_department, name='delete_department'),
]
