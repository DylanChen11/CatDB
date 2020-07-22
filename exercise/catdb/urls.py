from django.urls import path, include
from catdb import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter


# Create a router and register viewsets with it.
router=DefaultRouter()
router.register(r'homes', views.HomeViewSet)
router.register(r'humans', views.HumanViewSet)
router.register(r'cats', views.CatViewSet)
router.register(r'breeds', views.BreedViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = [
#     path('', views.api_root),
#     path('home/', views.HomeList.as_view(), name='home-list'),
#     path('home/<int:pk>/', views.HomeDetail.as_view(), name='home-detail'),
#     path('human/', views.HumanList.as_view(), name='human-list'),
#     path('human/<int:pk>/', views.HumanDetail.as_view(), name='human-detail'),
#     path('cat/', views.CatList.as_view(), name='cat-list'),
#     path('cat/<int:pk>/', views.CatDetail.as_view(), name='cat-detail'),
#     path('breed/', views.BreedList.as_view(), name='breed-list'),
#     path('breed/<int:pk>/', views.BreedDetail.as_view(), name='breed-detail'),
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)