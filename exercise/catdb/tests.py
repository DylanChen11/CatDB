import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

from .models import Breed, Cat, Home, Human
from .serializers import (BreedSerializer, CatSerializer, HomeSerializer,
                         HumanSerializer)

# Create your tests here.
class HomeViewSetTestCase(APITestCase):

    home_url=reverse("home-list")

    def setUp(self):
        self.user = User.objects.create_user(username= "test1", password="12345678")
        self.token= Token.objects.create(user= self.user)
        Home.objects.create(name="first house", address= "testaddr", Type="landed")
        Home.objects.create(name="second house", address= "testaddr2", Type="condo")

    #GET
    def test_home_list_authenticated(self):
        response= self.client.get(self.home_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #GET
    def test_home_detail_retrieve(self):
        response=self.client.get(reverse("home-detail", kwargs={"pk":1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "first house")
    
    #PUT
    def test_home_detail_update_authenticated(self):
        #change name of house
        client=APIClient()
        client.force_authenticate(user=self.user)
        response= client.put(reverse("home-detail", kwargs={"pk":1}), {"name":"second house"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response=client.get(reverse("home-detail", kwargs={"pk":1}))   #check if changes were made
        self.assertEqual(response.data["name"], "second house")
  

    def test_home_detail_update_unauthenticated(self):
        client=APIClient()
        #change name of house
        response= client.put(reverse("home-detail", kwargs={"pk":1}), {"name":"hacked"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    #POST
    def test_home_detail_add_authenticated(self):
        #change name of house
        client=APIClient()
        client.force_authenticate(user=self.user)
        response= client.post(reverse("home-list"), {"name":"third house", "address":"testaddr3", "Type":"condo"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response=client.get(reverse("home-detail", kwargs={"pk":3}))   #check if changes were made
        self.assertEqual(response.data["name"], "third house")
  

    def test_home_detail_add_unauthenticated(self):
        client=APIClient()
        #change name of house
        response= client.post(reverse("home-list"), {"name":"hacked house", "address":"fake addr", "Type":"condo"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #DELETE
    def test_home_detail_delete_authenticated(self):
        client=APIClient()
        client.force_authenticate(user=self.user)
        total_houses= len(self.client.get(reverse("home-list")).data)   #check no of houses atm
        response=client.delete(reverse("home-detail", kwargs={"pk":total_houses}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        total_houses_after_delete=len(self.client.get(reverse("home-list")).data)
        self.assertEqual(total_houses_after_delete, total_houses-1) #check if number of houses reduced

    def test_home_detail_delete_unauthenticated(self):
        client=APIClient()
        total_houses= len(self.client.get(reverse("home-list")).data)   #check no of houses atm
        response=client.delete(reverse("home-detail", kwargs={"pk":total_houses}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        total_houses_after_delete=len(self.client.get(reverse("home-list")).data)
        self.assertEqual(total_houses_after_delete, total_houses)  #check if number of houses is the same