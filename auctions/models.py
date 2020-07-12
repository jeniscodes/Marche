from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title=models.CharField(max_length=64)
    description=models.CharField(max_length=300)
    price=models.FloatField()
    Image=models.CharField(max_length=300)

    category=models.CharField(max_length=64)
    owner=models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    status=models.CharField(max_length=64)

    def __str__(self):
        return f" id : {self.id} title : {self.title}  owner: {self.owner}"

class Bid(models.Model):

    bid=models.IntegerField()

    item=models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="lbids")
    bidder=models.ForeignKey(User, on_delete=models.CASCADE, related_name="biditems")


    def __str__(self):
        return f"{self.item} was bidded from {self.bidder} "


class Comment(models.Model):

    comment=models.CharField(max_length=100)

    item=models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commenter=models.ForeignKey(User, on_delete=models.CASCADE, related_name="lcommenters")


    def __str__(self):
        return f"{self.item} was commented by {self.commenter} "

class Watchlist(models.Model):



    litem=models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="witems")
    luser=models.ForeignKey(User, on_delete=models.CASCADE, related_name="wuser")


    def __str__(self):
        return f"{self.litem} watchlisted by {self.luser} "
