from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

from decimal import Decimal

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions_created")
    title = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    image = models.URLField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="auctions_won")
    users_watching = models.ManyToManyField(User, blank=True, related_name="watchlisted")

    def __str__(self):
        return f"{self.title} ({self.owner}) {self.active}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])

    def __str__(self):
        return f"{self.listing} {self.user} {self.price}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title} ({self.user}): {self.text[:30]}"
