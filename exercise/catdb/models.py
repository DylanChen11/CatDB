from django.db import models

# Create your models here.

gender_choices = [
    ('M', 'Male'),
    ('F', 'Female'),
]

home_types = [
    ('landed', 'Landed'),
    ('condo', 'Condominium'),
]


class Breed(models.Model):
    name = models.CharField(max_length=100)
    origin = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(default='')

    def __str__(self):
        return "Name: "+self.name+", Origin: "+self.origin+", Desc: "+self.description


class Home(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    address = models.TextField(default='')
    # change this later to choices
    Type = models.CharField(max_length=10, choices=home_types, default='')

    def __str__(self):
        return "name: "+self.name+", address: " + self.address+", type: "+self.Type


class Human(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=gender_choices)
    # gender = models.CharField(max_length=6)  # change this later to choices
    dob = models.DateField()
    description = models.CharField(max_length=100, blank=True, default='')
    home = models.ForeignKey(
        Home, related_name='humans', on_delete=models.CASCADE)

    def __str__(self):
        return "Name: "+self.name+", gender: "+self.gender+", dob: "+str(self.dob)+", desc: "+self.description


class Cat(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=gender_choices)
    # gender = models.CharField(max_length=6)  # change this later to choices
    dob = models.DateField()
    description = models.TextField(default='')
    # related_name for reverse relationship
    breed = models.ForeignKey(
        Breed, related_name='cats', on_delete=models.CASCADE)
    owner = models.ForeignKey(
        Human, related_name='cats', on_delete=models.CASCADE)

    def get_home(self):
        return self.owner.home

    def __str__(self):
        return "Name: "+self.name+", gender: "+self.gender+", dob: "+str(self.dob)+", desc: "+self.description
