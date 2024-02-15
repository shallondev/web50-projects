from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# Model representing a listing item
class Listing(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='won_listings')

    def __str__(self):
        return self.title
    

# Model to represent categories
class Categories(models.Model):
    category = models.CharField(max_length=64, unique=True)
    listings = models.ManyToManyField(Listing, related_name='categories', blank=True)

    def __str__(self):
        return self.category
    

# Model to represent a user's watchlist
class WatchList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='watchlist')
    listings = models.ManyToManyField(Listing, related_name='watchlists', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Watchlist"
    

# Model to represent bids on a listing
class Bid(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, primary_key=True, related_name='bids') 
    user = models.ForeignKey(User, related_name='bids', on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Listing: {self.listing} Bid: {self.amount}"


# Model to represent comments on a listing
class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)  # Unique ID for each comment
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.title}"