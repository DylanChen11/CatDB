from rest_framework import serializers
from catdb.models import Home, Cat, Breed, Human


class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Home
        fields=['id', 'name', 'address', 'Type']

class HumanSerializer(serializers.ModelSerializer):
    class Meta:
        model=Human
        fields=['id', 'name', 'gender', 'dob', 'description', 'home']

class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cat
        fields=['id', 'name', 'gender', 'dob', 'description', 'breed', 'owner']

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model=Breed
        fields=['id', 'name', 'origin', 'description', 'homes']