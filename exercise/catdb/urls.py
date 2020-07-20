from django.urls import path
from catdb import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.api_root),
    path('home/', views.HomeList.as_view(), name='home-list'),
    path('home/<int:pk>/', views.HomeDetail.as_view(), name='home-detail'),
    path('human/', views.HumanList.as_view(), name='human-list'),
    path('human/<int:pk>/', views.HumanDetail.as_view(), name='human-detail'),
    path('cat/', views.CatList.as_view(), name='cat-list'),
    path('cat/<int:pk>/', views.CatDetail.as_view(), name='cat-detail'),
    path('breed/', views.BreedList.as_view(), name='breed-list'),
    path('breed/<int:pk>/', views.BreedDetail.as_view(), name='breed-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)