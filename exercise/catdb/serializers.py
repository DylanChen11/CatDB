from rest_framework import serializers
from catdb.models import Home, Cat, Breed, Human


class HomeSerializer(serializers.HyperlinkedModelSerializer):
    humans = serializers.HyperlinkedRelatedField(
        many=True, view_name='human-detail', read_only=True)

    class Meta:
        model = Home
        fields = ['id', 'name', 'address', 'Type', 'humans']


class HumanSerializer(serializers.HyperlinkedModelSerializer):
    cats = serializers.HyperlinkedRelatedField(
        many=True, view_name='cat-detail', read_only=True)

    class Meta:
        model = Human
        fields = ['id', 'name', 'gender', 'dob', 'description', 'home', 'cats']


class CatSerializer(serializers.HyperlinkedModelSerializer):
    home = serializers.CharField(source='owner.home.name', read_only=True)

    class Meta:
        model = Cat
        fields = ['id', 'name', 'gender', 'dob',
                  'description', 'breed', 'owner', 'home']


class BreedSerializer(serializers.HyperlinkedModelSerializer):
    cats = serializers.HyperlinkedRelatedField(
        many=True, view_name='cat-detail', read_only=True)
    # homes= CatSerializer(source='cats', many=True, read_only=True)

    # def get_homes(self, obj):
    #     print(obj.cats)
    #     return obj
    class Meta:
        model = Breed
        fields = ['id', 'name', 'origin', 'description', 'cats']
