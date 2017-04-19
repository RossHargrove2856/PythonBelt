from django.shortcuts import render, redirect
from models import Item
from ..login_and_reg.models import User

# This renders the page to add an item
def createItem(request):
    user = User.objects.get(id=request.session["logged_in"])
    context = {
        "user": user
    }
    return render(request, "wishlist_app/addItem.html", context)

# This processes the add item from and redirects back to the same page if there was an error or back to the dashboard if the add was successful
def addItem(request):
    # Calls the create method of the ItemManager class
    new_item = Item.item_manager.create(request)
    if not new_item:
        return redirect("/wishlist_app/createItem")
    else:
        return redirect("/success")

# This renders a page with item information from the dashboard
def itemInfo(request, item_id):
    item = Item.objects.get(id=item_id)
    users = item.item_user.all()
    user = User.objects.get(id=request.session["logged_in"])
    context = {
        "item": item,
        "users": users,
        "user": user
    }
    return render(request, "wishlist_app/itemInfo.html", context)

# This processes adding an item to a user's wishlist and redirects to the dashboard
def addWishlist(request, item_id):
    # Calls the addWishlist method of the ItemManager class
    added_item = Item.item_manager.addWishlist(request, item_id)
    return redirect("/success")

# This processes removing an item from a user's wishlist and redirecting to the dashboard
def removeWishlist(request, item_id):
    # Calls the removeWishlist method of the ItemManager class
    removed_item = Item.item_manager.removeWishlist(request, item_id)
    return redirect("/success")

# This processes deleleting an item from the database entirely and redirecting to the dashboards
def destroy(request, item_id):
    destroyed_item = Item.objects.get(id=item_id)
    destroyed_item.delete()
    return redirect("/success")
