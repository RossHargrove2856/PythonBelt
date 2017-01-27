from django.shortcuts import render, redirect
from models import Item

def createItem(request):
    return render(request, "myBelt/addItem.html")

def addItem(request):
    new_item = Item.item_manager.create(request)
    if not new_item:
        return request("/belt/addItem")
    else:
        return redirect("/success")

def itemInfo(request, item_id):
    items = Item.objects.get(id=item_id)
    context = {
        "items": items
    }
    return render(request, "myBelt/itemInfo.html", context)

def addWishlist(request, item_id):
    added_item = Item.item_manager.addWishlist(request, item_id)
    return redirect("/success")

def removeWishlist(request, item_id):
    removed_item = Item.item_manager.removeWishlist(request, item_id)
    return redirect("/success")

def destroy(request, item_id):
    destroyed_item = Item.objects.get(id=item_id)
    destroyed_item.delete()
    return redirect("/success")