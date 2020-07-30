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

    def setUp(self):
        self.user = User.objects.create_user(
            username="test1", password="12345678")
        self.token = Token.objects.create(user=self.user)
        Home.objects.create(name="first house",
                            address="testaddr", Type="landed")
        Home.objects.create(name="second house",
                            address="testaddr2", Type="condo")

    # GET
    def test_home_list_retrieve(self):
        response = self.client.get(reverse("home-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.client.get(reverse("home-list")).data), 2)
        self.assertEqual(self.client.get(reverse("home-list")).data[0]["name"], "first house")
        self.assertEqual(self.client.get(reverse("home-list")).data[0]["address"], "testaddr")
        self.assertEqual(self.client.get(reverse("home-list")).data[0]["Type"], "landed")
        self.assertEqual(self.client.get(reverse("home-list")).data[1]["name"], "second house")
        self.assertEqual(self.client.get(reverse("home-list")).data[1]["address"], "testaddr2")
        self.assertEqual(self.client.get(reverse("home-list")).data[1]["Type"], "condo")


    # GET
    def test_home_detail_retrieve(self):
        response = self.client.get(reverse("home-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "first house")
        self.assertEqual(response.data["address"], "testaddr")
        self.assertEqual(response.data["Type"], "landed")

    # PUT
    def test_home_detail_update_authenticated(self):
        # change name of house
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.put(
            reverse("home-detail", kwargs={"pk": 1}), {"name": "second house"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check if changes were made
        response = client.get(reverse("home-detail", kwargs={"pk": 1}))
        self.assertEqual(response.data["name"], "second house")

    def test_home_detail_update_unauthenticated(self):
        client = APIClient()
        # change name of house
        response = client.put(
            reverse("home-detail", kwargs={"pk": 1}), {"name": "hacked"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # POST

    def test_home_detail_add_authenticated(self):
        # change name of house
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse(
            "home-list"), {"name": "third house", "address": "testaddr3", "Type": "condo"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check if changes were made
        total_houses = len(self.client.get(reverse("home-list")).data)
        response = client.get(
            reverse("home-detail", kwargs={"pk": total_houses}))
        self.assertEqual(response.data["name"], "third house")
        self.assertEqual(response.data["address"], "testaddr3")
        self.assertEqual(response.data["Type"], "condo")


    def test_home_detail_add_unauthenticated(self):
        client = APIClient()
        # change name of house
        response = client.post(reverse(
            "home-list"), {"name": "hacked house", "address": "fake addr", "Type": "condo"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # DELETE
    def test_home_detail_delete_authenticated(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        # check no of houses atm
        total_houses = len(self.client.get(reverse("home-list")).data)
        response = client.delete(
            reverse("home-detail", kwargs={"pk": total_houses}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        total_houses_after_delete = len(
            self.client.get(reverse("home-list")).data)
        # check if number of houses reduced
        self.assertEqual(total_houses_after_delete, total_houses-1)

    def test_home_detail_delete_unauthenticated(self):
        client = APIClient()
        # check no of houses atm
        total_houses = len(self.client.get(reverse("home-list")).data)
        response = client.delete(
            reverse("home-detail", kwargs={"pk": total_houses}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        total_houses_after_delete = len(
            self.client.get(reverse("home-list")).data)
        # check if number of houses is the same
        self.assertEqual(total_houses_after_delete, total_houses)

    def test_home_not_found(self):
        response = self.client.get(reverse("home-detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BreedViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test1", password="12345678")
        self.token = Token.objects.create(user=self.user)
        Breed.objects.create(
            name="Munchkin", origin="Mutation", description="Dwarf")
        Breed.objects.create(name="Bengal", origin="Hybrid of the Abyssinian and Egyptian Mau x leopard cat",
                             description="Spotted, marbled, or rosetted")

    # GET

    def test_breed_list_retrieve(self):
        response = self.client.get(reverse("breed-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.client.get(reverse("breed-list")).data), 2)
        self.assertEqual(self.client.get(reverse("breed-list")).data[0]["name"], "Munchkin")
        self.assertEqual(self.client.get(reverse("breed-list")).data[0]["origin"], "Mutation")
        self.assertEqual(self.client.get(reverse("breed-list")).data[0]["description"], "Dwarf")
        self.assertEqual(self.client.get(reverse("breed-list")).data[1]["name"], "Bengal")
        self.assertEqual(self.client.get(reverse("breed-list")).data[1]["origin"], "Hybrid of the Abyssinian and Egyptian Mau x leopard cat")
        self.assertEqual(self.client.get(reverse("breed-list")).data[1]["description"], "Spotted, marbled, or rosetted")


    # GET
    def test_breed_detail_retrieve(self):
        response = self.client.get(reverse("breed-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Munchkin")
        self.assertEqual(response.data["origin"], "Mutation")
        self.assertEqual(response.data["description"], "Dwarf")

    # PUT
    def test_breed_detail_update_authenticated(self):
        # change name of breed
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.put(
            reverse("breed-detail", kwargs={"pk": 1}), {"name": "Abyssinian"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check if changes were made
        response = client.get(reverse("breed-detail", kwargs={"pk": 1}))
        self.assertEqual(response.data["name"], "Abyssinian")

    def test_breed_detail_update_unauthenticated(self):
        client = APIClient()
        # change name of breed
        response = client.put(
            reverse("breed-detail", kwargs={"pk": 1}), {"name": "hacked"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # POST

    def test_breed_detail_add_authenticated(self):
        # change name of breed
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse(
            "breed-list"), {"name": "another breed", "origin": "another origin", "description": "another desc", })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check if changes were made
        total_breeds = len(self.client.get(reverse("breed-list")).data)
        response = client.get(
            reverse("breed-detail", kwargs={"pk": total_breeds}))
        self.assertEqual(response.data["name"], "another breed")
        self.assertEqual(response.data["origin"], "another origin")
        self.assertEqual(response.data["description"], "another desc")


    def test_breed_detail_add_unauthenticated(self):
        client = APIClient()
        # change name of breed
        response = client.post(reverse(
            "breed-list"), {"name": "hacked breed", "address": "fake addr", "Type": "condo"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # DELETE
    def test_breed_detail_delete_authenticated(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        # check no of houses atm
        total_breeds = len(self.client.get(reverse("breed-list")).data)
        response = client.delete(
            reverse("breed-detail", kwargs={"pk": total_breeds}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        total_breeds_after_delete = len(
            self.client.get(reverse("breed-list")).data)
        # check if number of breeds reduced
        self.assertEqual(total_breeds_after_delete, total_breeds-1)

    def test_breed_detail_delete_unauthenticated(self):
        client = APIClient()
        # check no of breeds atm
        total_breeds = len(self.client.get(reverse("breed-list")).data)
        response = client.delete(
            reverse("breed-detail", kwargs={"pk": total_breeds}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        total_breeds_after_delete = len(
            self.client.get(reverse("breed-list")).data)
        # check if number of breeds is the same
        self.assertEqual(total_breeds_after_delete, total_breeds)

    def test_breed_not_found(self):
        response = self.client.get(reverse("breed-detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class HumanViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test1", password="12345678")
        self.token = Token.objects.create(user=self.user)
        Home.objects.create(name="first house",
                            address="testaddr", Type="landed")
        Home.objects.create(name="second house",
                            address="testaddr2", Type="condo")
        Human.objects.create(name="dylan", gender="M", dob="1998-01-12",
                             description="dog lover", home=Home.objects.get(pk=1))
        Human.objects.create(name="thereisa", gender="F", dob="1948-07-16",
                             description="dylan's grandma", home=Home.objects.get(pk=2))

    # GET

    def test_human_list_retrieve(self):
        response = self.client.get(reverse("human-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.client.get(reverse("human-list")).data), 2)
        self.assertEqual(self.client.get(reverse("human-list")).data[0]["name"], "dylan")
        self.assertEqual(self.client.get(reverse("human-list")).data[0]["gender"], "M")
        self.assertEqual(self.client.get(reverse("human-list")).data[0]["dob"], "1998-01-12")
        self.assertEqual(self.client.get(reverse("human-list")).data[0]["description"], "dog lover")
        self.assertEqual(self.client.get(reverse("human-list")).data[0]["home"], "http://testserver/homes/1/")
        self.assertEqual(self.client.get(reverse("human-list")).data[1]["name"], "thereisa")
        self.assertEqual(self.client.get(reverse("human-list")).data[1]["gender"], "F")
        self.assertEqual(self.client.get(reverse("human-list")).data[1]["dob"], "1948-07-16")
        self.assertEqual(self.client.get(reverse("human-list")).data[1]["description"], "dylan's grandma")
        self.assertEqual(self.client.get(reverse("human-list")).data[1]["home"], "http://testserver/homes/2/")
        

    # GET
    def test_human_detail_retrieve(self):
        response = self.client.get(reverse("human-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "dylan")
        self.assertEqual(response.data["gender"], "M")
        self.assertEqual(response.data["dob"], "1998-01-12")
        self.assertEqual(response.data["description"], "dog lover")
        self.assertEqual(response.data["home"], "http://testserver/homes/1/")

    # PUT
    def test_human_detail_update_authenticated(self):
        # change name of human
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.put(
            reverse("human-detail", kwargs={"pk": 1}), {"name": "mark", "gender": "M", "dob": "2006-02-15", "description": "test", "home": "http://testserver/homes/1/"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check if changes were made
        response = client.get(reverse("human-detail", kwargs={"pk": 1}))
        self.assertEqual(response.data["name"], "mark")
        self.assertEqual(response.data["gender"], "M")
        self.assertEqual(response.data["dob"], "2006-02-15")
        self.assertEqual(response.data["description"], "test")
        self.assertEqual(response.data["home"], "http://testserver/homes/1/")

    def test_human_detail_update_unauthenticated(self):
        client = APIClient()
        # change name of human
        response = client.put(
            reverse("human-detail", kwargs={"pk": 1}), {"name": "hacked"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # POST

    def test_human_detail_add_authenticated(self):
        # change name of human
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse(
            "human-list"), {"name": "alice", "gender": "F", "dob": "2000-01-12", "description": "cat lover", "home": "http://testserver/homes/2/"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check if changes were made
        total_humans = len(self.client.get(reverse("human-list")).data)
        response = client.get(
            reverse("human-detail", kwargs={"pk": total_humans}))
        self.assertEqual(response.data["name"], "alice")
        self.assertEqual(response.data["gender"], "F")
        self.assertEqual(response.data["dob"], "2000-01-12")
        self.assertEqual(response.data["description"], "cat lover")
        self.assertEqual(response.data["home"], "http://testserver/homes/2/")

    def test_human_detail_add_unauthenticated(self):
        client = APIClient()
        # change name of human
        response = client.post(reverse(
            "human-list"), {"name": "hacker name", " gender": "M", "dob": "2000-01-12", "description": "hacker", "home": "http://testserver/homes/1/"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # DELETE
    def test_human_detail_delete_authenticated(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        # check no of houses atm
        total_humans = len(self.client.get(reverse("human-list")).data)
        response = client.delete(
            reverse("human-detail", kwargs={"pk": total_humans}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        total_humans_after_delete = len(
            self.client.get(reverse("human-list")).data)
        # check if number of human reduced
        self.assertEqual(total_humans_after_delete, total_humans-1)

    def test_human_detail_delete_unauthenticated(self):
        client = APIClient()
        # check no of human atm
        total_humans = len(self.client.get(reverse("human-list")).data)
        response = client.delete(
            reverse("human-detail", kwargs={"pk": total_humans}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        total_humans_after_delete = len(
            self.client.get(reverse("human-list")).data)
        # check if number of humans is the same
        self.assertEqual(total_humans_after_delete, total_humans)

    def test_human_not_found(self):
        response = self.client.get(reverse("human-detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CatViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test1", password="12345678")
        self.token = Token.objects.create(user=self.user)
        Home.objects.create(name="first house",
                            address="testaddr", Type="landed")
        Home.objects.create(name="second house",
                            address="testaddr2", Type="condo")
        Human.objects.create(name="dylan", gender="M", dob="1998-01-12",
                             description="dog lover", home=Home.objects.get(pk=1))
        Human.objects.create(name="thereisa", gender="F", dob="1948-07-16",
                             description="dylan's grandma", home=Home.objects.get(pk=2))
        Breed.objects.create(
            name="Munchkin", origin="Mutation", description="Dwarf")
        Breed.objects.create(name="Bengal", origin="Hybrid of the Abyssinian and Egyptian Mau x leopard cat",
                             description="Spotted, marbled, or rosetted")
        Cat.objects.create(name="bobby", gender="M", dob="2014-02-20", description="brown cat",
                           breed=Breed.objects.get(pk=1), owner=Human.objects.get(pk=1))
        Cat.objects.create(name="tom", gender="M", dob="2016-07-16", description="grey cat",
                           breed=Breed.objects.get(pk=2), owner=Human.objects.get(pk=2))

    # GET

    def test_cat_list_retrieve(self):
        response = self.client.get(reverse("cat-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.client.get(reverse("cat-list")).data), 2)
        self.assertEqual(self.client.get(reverse("cat-list")).data[0]["name"], "bobby")
        self.assertEqual(self.client.get(reverse("cat-list")).data[0]["gender"], "M")
        self.assertEqual(self.client.get(reverse("cat-list")).data[0]["dob"], "2014-02-20")
        self.assertEqual(self.client.get(reverse("cat-list")).data[0]["description"], "brown cat")
        self.assertEqual(self.client.get(reverse("cat-list")).data[0]["breed"], "http://testserver/breeds/1/")
        self.assertEqual(self.client.get(reverse("cat-list")).data[0]["owner"], "http://testserver/humans/1/")
        self.assertEqual(self.client.get(reverse("cat-list")).data[1]["name"], "tom")
        self.assertEqual(self.client.get(reverse("cat-list")).data[1]["gender"], "M")
        self.assertEqual(self.client.get(reverse("cat-list")).data[1]["dob"], "2016-07-16")
        self.assertEqual(self.client.get(reverse("cat-list")).data[1]["description"], "grey cat")
        self.assertEqual(self.client.get(reverse("cat-list")).data[1]["breed"], "http://testserver/breeds/2/")
        self.assertEqual(self.client.get(reverse("cat-list")).data[1]["owner"], "http://testserver/humans/2/")

    # GET
    def test_cat_detail_retrieve(self):
        response = self.client.get(reverse("cat-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "bobby")
        self.assertEqual(response.data["gender"], "M")
        self.assertEqual(response.data["dob"], "2014-02-20")
        self.assertEqual(response.data["description"], "brown cat")
        self.assertEqual(response.data["breed"], "http://testserver/breeds/1/")
        self.assertEqual(response.data["owner"], "http://testserver/humans/1/")


    # PUT
    def test_cat_detail_update_authenticated(self):
        # change name of cat
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.put(
            reverse("cat-detail", kwargs={"pk": 1}), {"name": "shiro", "gender": "F", "dob": "1999-08-16", "description": "white cat", "breed": "http://testserver/breeds/1/", "owner": "http://testserver/humans/1/"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check if changes were made
        response = client.get(reverse("cat-detail", kwargs={"pk": 1}))
        self.assertEqual(response.data["name"], "shiro")
        self.assertEqual(response.data["gender"], "F")
        self.assertEqual(response.data["dob"], "1999-08-16")
        self.assertEqual(response.data["description"], "white cat")
        self.assertEqual(response.data["breed"], "http://testserver/breeds/1/")
        self.assertEqual(response.data["owner"], "http://testserver/humans/1/")


    def test_cat_detail_update_unauthenticated(self):
        client = APIClient()
        # change name of cat
        response = client.put(
            reverse("cat-detail", kwargs={"pk": 1}), {"name": "hacked"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # POST

    def test_cat_detail_add_authenticated(self):
        # change name of cat
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse(
            "cat-list"), {"name": "kuro", "gender": "M", "dob": "2000-01-18", "description": "black cat", "breed": "http://testserver/breeds/2/", "owner": "http://testserver/humans/2/"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check if changes were made
        total_cats = len(self.client.get(reverse("cat-list")).data)
        response = client.get(
            reverse("cat-detail", kwargs={"pk": total_cats}))
        self.assertEqual(response.data["name"], "kuro")
        self.assertEqual(response.data["gender"], "M")
        self.assertEqual(response.data["dob"], "2000-01-18")
        self.assertEqual(response.data["description"], "black cat")
        self.assertEqual(response.data["breed"], "http://testserver/breeds/2/")
        self.assertEqual(response.data["owner"], "http://testserver/humans/2/")
        

    def test_cat_detail_add_unauthenticated(self):
        client = APIClient()
        # change name of cat
        response = client.post(reverse(
            "cat-list"), {"name": "hacked", "gender": "M", "dob": "2000-01-18", "description": "hacked cat", "breed": "http://testserver/breeds/1/", "owner": "http://testserver/humans/2/"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # DELETE
    def test_cat_detail_delete_authenticated(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        # check no of houses atm
        total_cats = len(self.client.get(reverse("cat-list")).data)
        response = client.delete(
            reverse("cat-detail", kwargs={"pk": total_cats}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        total_cats_after_delete = len(
            self.client.get(reverse("cat-list")).data)
        # check if number of cat reduced
        self.assertEqual(total_cats_after_delete, total_cats-1)

    def test_cat_detail_delete_unauthenticated(self):
        client = APIClient()
        # check no of cat atm
        total_cats = len(self.client.get(reverse("cat-list")).data)
        response = client.delete(
            reverse("cat-detail", kwargs={"pk": total_cats}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        total_cats_after_delete = len(
            self.client.get(reverse("cat-list")).data)
        # check if number of cats is the same
        self.assertEqual(total_cats_after_delete, total_cats)

    def test_cat_not_found(self):
        response = self.client.get(reverse("cat-detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
