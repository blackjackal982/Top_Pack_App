from django.db import models

# Create your models here.

class Package(models.Model):
    name = models.CharField(max_length=256)
    count = models.IntegerField()

    def __str__(self):
        return self.name

class Repo(models.Model):
    owner = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    stars = models.IntegerField()
    dep = models.ForeignKey(Package,on_delete=models.CASCADE)

    def __str__(self):
        return self.name



