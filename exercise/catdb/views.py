from django.shortcuts import render
from rest_framework import generics
from catdb.models import Home, Human, Cat, Breed
from catdb.serializers import HomeSerializer, HumanSerializer, CatSerializer, BreedSerializer
# Create your views here.



class HomeList(generics.ListCreateAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer


class HomeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer

class HumanList(generics.ListCreateAPIView):
    queryset = Human.objects.all()
    serializer_class = HumanSerializer


class HumanDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Human.objects.all()
    serializer_class = HumanSerializer

class CatList(generics.ListCreateAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class CatDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

class BreedList(generics.ListCreateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class BreedDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
# @csrf_exempt
# def homes_list(request):
#     """
#     List all houses, or create a new house.
#     """
#     if request.method == 'GET':
#         homes = Home.objects.all()
#         serializer = HomeSerializer(homes, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = HomeSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def home_detail(request, pk):
#     """
#     Retrieve, update or delete a house instance.
#     """
#     try:
#         home = Home.objects.get(pk=pk)
#     except home.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = HomeSerializer(home)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = HomeSerializer(home, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         home.delete()
#         return HttpResponse(status=204)


# @csrf_exempt
# def human_list(request):
#     """
#     List all houses, or create a new human.
#     """
#     if request.method == 'GET':
#         humans = Human.objects.all()
#         serializer = HumanSerializer(humans, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = HumanSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def human_detail(request, pk):
#     """
#     Retrieve, update or delete a human instance.
#     """
#     try:
#         human = Human.objects.get(pk=pk)
#     except human.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = HumanSerializer(human)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = HumanSerializer(human, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         human.delete()
#         return HttpResponse(status=204)

# @csrf_exempt
# def cat_list(request):
#     """
#     List all houses, or create a new cat.
#     """
#     if request.method == 'GET':
#         cats = Cat.objects.all()
#         serializer = CatSerializer(cats, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = CatSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def cat_detail(request, pk):
#     """
#     Retrieve, update or delete a cat instance.
#     """
#     try:
#         cat = Cat.objects.get(pk=pk)
#     except cat.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = CatSerializer(cat)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = CatSerializer(cat, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         cat.delete()
#         return HttpResponse(status=204)

# @csrf_exempt
# def breed_list(request):
#     """
#     List all houses, or create a new breed.
#     """
#     if request.method == 'GET':
#         breeds = Breed.objects.all()
#         serializer = BreedSerializer(breeds, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = BreedSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def breed_detail(request, pk):
#     """
#     Retrieve, update or delete a breed instance.
#     """
#     try:
#         breed = Breed.objects.get(pk=pk)
#     except breed.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = BreedSerializer(breed)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = BreedSerializer(breed, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         breed.delete()
#         return HttpResponse(status=204) 