from django.urls import path
from catdb import views

urlpatterns = [
    path('homes/', views.homes_list),
    path('homes/<int:pk>/', views.home_detail),
    path('human/', views.human_list),
    path('human/<int:pk>/', views.human_detail),
    path('cat/', views.cat_list),
    path('cat/<int:pk>/', views.cat_detail),
    path('breed/', views.breed_list),
    path('breed/<int:pk>/', views.breed_detail),
]