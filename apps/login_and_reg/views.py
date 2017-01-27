from django.shortcuts import render, redirect
from models import User
from ..myBelt.models import Item

def index(request):
    return render(request, "login_and_reg/index.html")

def register(request):
    registered_user = User.usermanager.register(request)
    if not registered_user:
        return redirect("/")
    else:
        return redirect("/success")

def login(request):
    logged_user = User.usermanager.login(request)
    if not logged_user:
        return redirect("/")
    else:
        return redirect("/success")

def success(request):
    user = User.objects.get(id=request.session["logged_in"])
    other_items = Item.objects.exclude(logged_user=user)
    user_items = user.item_set.all()
    context = {
        "user":user,
        "other_items": other_items,
        "user_items": user_items
    }
    return render(request, "login_and_reg/success.html", context)

def logout(request):
    del request.session["logged_in"]
    return redirect("/")