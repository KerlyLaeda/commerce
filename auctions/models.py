from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


# class Bid(models.Model):
#     listing = models.ForeignKey('AuctionListing', on_delete=models.CASCADE)
#     bid = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
#     bidder = models.ForeignKey(User, on_delete=models.CASCADE)


class AuctionListing(models.Model):
    class AuctionCategory(models.TextChoices):
        HOME = "Home"
        FASHION = "Fashion"
        TOYS = "Toys"
        ELECTRONICS = "Electronics"
        PETS = "Pets"
        OTHER = "Other"

    title = models.CharField(max_length=64)
    description = models.TextField()
    # price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bid_amount")
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    date_posted = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(blank=True, null=True, default='default_item_image.jpg')
    category = models.CharField(max_length=64, blank=True, null=True,
                                choices=AuctionCategory.choices)
    # is_active = models.BooleanField(default=True)
    # in_wishlist = models.

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # why delete comments?
    date_posted = models.DateTimeField(default=timezone.now)






# testuser testing0000
