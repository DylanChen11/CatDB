from django.urls import path
from catdb import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('home/', views.HomeList.as_view()),
    path('home/<int:pk>/', views.HomeDetail.as_view()),
    path('human/', views.HumanList.as_view()),
    path('human/<int:pk>/', views.HumanDetail.as_view()),
    path('cat/', views.CatList.as_view()),
    path('cat/<int:pk>/', views.CatDetail.as_view()),
    path('breed/', views.BreedList.as_view()),
    path('breed/<int:pk>/', views.BreedDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)