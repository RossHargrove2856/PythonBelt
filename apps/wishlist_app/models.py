from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from ..login_and_reg.models import User

# Item Manager for methods to query the DB
class ItemManager(models.Manager):
    # The method to create a new item
    def create(self, request):
        # Validation to make sure entry is not blank and is longer than 3 characters. A flag, isValid, is used to make all the checks
        isValid = True
        if len(request.POST["new_item"]) == 0:
            messages.error(request, "Item Name cannot be blank")
            isValid = False
        if len(request.POST["new_item"]) < 4:
            messages.error(request, "Item Name has to be longer than 3 characters")
            isValid = False
        if not isValid:
            return False
        # If the validation passes, the item is created and saved to the DB
        new_item = Item (name=request.POST["new_item"], logged_user=User.objects.get(id = request.session["logged_in"]))
        new_item.save()
        new_item.item_user.add(new_item.logged_user)
        return True

    # The method to add an association between a user and an item in the DB
    def addWishlist(self, request, item_id):
        added_item = Item.objects.get(id = item_id)
        added_user = User.objects.get(id = request.session["logged_in"])
        added_item.item_user.add(added_user)
        return True

    # The method to remove an item from being associated with a user in the DB
    def removeWishlist(self, request, item_id):
        removed_user = User.objects.get(id = request.session["logged_in"])
        Item.objects.get(id = item_id).item_user.remove(removed_user)
        return True

# The model for items, with the item_manager for DB methods, logged_user and item_user for relationships with the User model
class Item(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    objects = models.Manager()
    item_manager = ItemManager()
    logged_user = models.ForeignKey(User, related_name = "logged_item")
    item_user = models.ManyToManyField(User)
