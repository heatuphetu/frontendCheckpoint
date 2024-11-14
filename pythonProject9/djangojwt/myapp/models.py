from django.db import models
from django.contrib.auth.models import User

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, null=True, blank=True)

    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    available_to_deliver = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="books")
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, default='Unknown Author')
    publication_date = models.DateField(blank=True, null=True)
    publisher_name = models.CharField(max_length=100, blank=True, null=True)
    edition = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    condition = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
