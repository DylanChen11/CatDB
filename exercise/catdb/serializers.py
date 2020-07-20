from rest_framework import serializers
from catdb.models import Home, Cat, Breed, Human


class HomeSerializer(serializers.HyperlinkedModelSerializer):
    humans=serializers.HyperlinkedRelatedField(many=True, view_name='human-detail', read_only=True)
    class Meta:
        model=Home
        fields=['id', 'name', 'address', 'Type', 'humans']

class HumanSerializer(serializers.HyperlinkedModelSerializer):
    cats=serializers.HyperlinkedRelatedField(many=True, view_name='cat-detail', read_only=True)
    class Meta:
        model=Human
        fields=['id', 'name', 'gender', 'dob', 'description', 'home', 'cats']

class CatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Cat
        fields=['id', 'name', 'gender', 'dob', 'description', 'breed', 'owner']

class BreedSerializer(serializers.HyperlinkedModelSerializer):
    cats=serializers.HyperlinkedRelatedField(many=True, view_name='cat-detail', read_only=True)
    class Meta:
        model=Breed
        fields=['id', 'name', 'origin', 'description', 'homes', 'cats']