from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from ..login_and_reg.models import User

class ItemManager(models.Manager):
    def create(self, request):
        isValid = True
        if len(request.POST["new_item"]) == 0:
            messages.error(request, "Item Name cannot be blank")
            isValid = False
        if len(request.POST["new_item"]) < 4:
            messages.error(request, "Item Name has to be longer than 3 characters")
            isValid = False
        if not isValid:
            return False
        new_item = Item (name=request.POST["new_item"], logged_user=User.objects.get(id = request.session["logged_in"]))
        new_item.save()
        new_item.item_user.add(new_item.logged_user)
        return True

    def addWishlist(self, request, item_id):
        added_item = Item.objects.get(id = item_id)
        added_user = User.objects.get(id = request.session["logged_in"])
        added_item.item_user.add(added_user)
        return True

    def removeWishlist(self, request, item_id):
        removed_item = Item.objects.get(id = item_id)
        removed_user = User.objects.get(id = request.session["logged_in"])
        removed_item.logged_user.delete(str(removed_user))
        return True

class Item(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    objects = models.Manager()
    item_manager = ItemManager()
    logged_user = models.ForeignKey(User, related_name = "logged_item")
    item_user = models.ManyToManyField(User)