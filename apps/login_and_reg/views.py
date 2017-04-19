from django.shortcuts import render, redirect
from models import User
from ..wishlist_app.models import Item

# This renders the index page with login and registration forms
def index(request):
    return render(request, "login_and_reg/index.html")

# This is a redirect for registration to the index view if unsuccesful or the dashboard view if successful
def register(request):
    # Calls the register method of the UserManager class
    registered_user = User.user_manager.register(request)
    if not registered_user:
        return redirect("/")
    else:
        return redirect("/success")

# This is a redirect for the login to the index view if unsuccesful or the dashboard view if successful
def login(request):
    # Calls the login method of the UserManager class
    logged_user = User.user_manager.login(request)
    if not logged_user:
        return redirect("/")
    else:
        return redirect("/success")

# This renders the dashboard after login or registration
def success(request):
    user = User.objects.get(id=request.session["logged_in"])
    other_items = Item.objects.exclude(item_user=user)
    user_items = user.item_set.all()
    context = {
        "user": user,
        "other_items": other_items,
        "user_items": user_items,
        "session": request.session["logged_in"]
    }
    return render(request, "login_and_reg/success.html", context)

# This renders user infromation from a user link on the dashboard
def userInfo(request, user_id):
    user = User.objects.get(id=user_id)
    items = user.item_set.all()
    logged_user = User.objects.get(id=request.session["logged_in"])
    context = {
        "user": user,
        "items": items,
        "logged_user": logged_user
    }
    return render(request, "login_and_reg/user_info.html", context)

# This deletes user information from session to log the user out and redirects to the index view to log in or register
def logout(request):
    del request.session["logged_in"]
    return redirect("/")