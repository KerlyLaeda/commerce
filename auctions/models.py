from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Bid(models.Model):
    bid = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey('AuctionListing', on_delete=models.CASCADE, related_name="listing_bids")


class AuctionListing(models.Model):
    class AuctionCategory(models.TextChoices):
        HOME = "Home"
        FASHION = "Fashion"
        TOYS = "Toys"
        ELECTRONICS = "Electronics"
        PETS = "Pets"
        SPORT = "Sport"
        OTHER = "Other"

    title = models.CharField(max_length=64)
    description = models.TextField()
    # price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bid_amount")
    price = models.DecimalField(max_digits=20, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    date_posted = models.DateTimeField(default=timezone.now)
    photo = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=64, blank=True, null=True,
                                choices=AuctionCategory.choices)
    is_active = models.BooleanField(default=True)
    in_watchlist = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_comments")

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f"{self.author} commented on {self.listing}, {self.date_posted}."
