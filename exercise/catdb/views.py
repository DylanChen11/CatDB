from django.shortcuts import render
from rest_framework import generics
from catdb.models import Home, Human, Cat, Breed
from catdb.serializers import HomeSerializer, HumanSerializer, CatSerializer, BreedSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework import viewsets
# Create your views here.


class HomeViewSet(viewsets.ModelViewSet):
    # This viewset automatically provides `list`, `create`, `retrieve`,
    # `update` and `destroy` actions.
    queryset = Home.objects.all()
    serializer_class = HomeSerializer


class HumanViewSet(viewsets.ModelViewSet):
    queryset = Human.objects.all()
    serializer_class = HumanSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


# class HomeList(generics.ListCreateAPIView):
#     queryset = Home.objects.all()
#     serializer_class = HomeSerializer


# class HomeDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Home.objects.all()
#     serializer_class = HomeSerializer

# class HumanList(generics.ListCreateAPIView):
#     queryset = Human.objects.all()
#     serializer_class = HumanSerializer


# class HumanDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Human.objects.all()
#     serializer_class = HumanSerializer

# class CatList(generics.ListCreateAPIView):
#     queryset = Cat.objects.all()
#     serializer_class = CatSerializer


# class CatDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Cat.objects.all()
#     serializer_class = CatSerializer

# class BreedList(generics.ListCreateAPIView):
#     queryset = Breed.objects.all()
#     serializer_class = BreedSerializer


# class BreedDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Breed.objects.all()
#     serializer_class = BreedSerializer
