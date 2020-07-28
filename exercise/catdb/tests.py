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

    # GET
    def test_home_detail_retrieve(self):
        response = self.client.get(reverse("home-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "first house")

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

    # GET
    def test_breed_detail_retrieve(self):
        response = self.client.get(reverse("breed-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Munchkin")

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

    # GET
    def test_human_detail_retrieve(self):
        response = self.client.get(reverse("human-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "dylan")

    # PUT
    def test_human_detail_update_authenticated(self):
        # change name of human
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.put(
            reverse("human-detail", kwargs={"pk": 1}), {"name": "mark", "gender": "M", "dob": "2006-02-15", "description": "test", "home": "http://localhost:8000/homes/1/"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check if changes were made
        response = client.get(reverse("human-detail", kwargs={"pk": 1}))
        self.assertEqual(response.data["name"], "mark")

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
            "human-list"), {"name": "alice", "gender": "F", "dob": "2000-01-12", "description": "cat lover", "home": "http://localhost:8000/homes/1/"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check if changes were made
        total_humans = len(self.client.get(reverse("human-list")).data)
        response = client.get(
            reverse("human-detail", kwargs={"pk": total_humans}))
        self.assertEqual(response.data["name"], "alice")

    def test_human_detail_add_unauthenticated(self):
        client = APIClient()
        # change name of human
        response = client.post(reverse(
            "human-list"), {"name": "hacker name", " gender": "M", "dob": "2000-01-12", "description": "hacker", "home": "http://localhost:8000/homes/1/"})
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
