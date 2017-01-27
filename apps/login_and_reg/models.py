from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt

class UserManager(models.Manager):
    def register(self, request):
        isValid = True
        if len(request.POST["first_name"]) < 3:
            messages.error(request, "Name required, has to be more than 1 character")
            isValid = False
        if str.isalpha(str(request.POST["first_name"])) == False:
            messages.error(request, "Name can only be letters")
            isValid = False
        if len(request.POST["username"]) < 3:
            messages.error(request, "Username required")
            isValid = False
        email_compare = User.objects.filter(username=request.POST["username"])
        if len(email_compare) > 0:
            messages.error(request, "This username is already registered")
            isValid = False
        if len(request.POST["password"]) < 6:
            messages.error(request, "Password cannot be less than 6 characters")
            isValid = False
        if request.POST["password"] != request.POST["confirmpw"]:
            messages.error(request, "Password does not match Confirmed Password")
            isValid = False
        if not isValid:
            return False

        hashed_pw = bcrypt.hashpw(request.POST["password"].encode("utf-8"), bcrypt.gensalt())
        new_user = User (
                first_name = request.POST["first_name"],
                username = request.POST["username"],
                pw_hashed = hashed_pw,
            )
        new_user.save()

        request.session["logged_in"] = new_user.id

        return True

    def login(self, request):
        isValid = True
        user = User.objects.get(username=request.POST["username"])
        if len(user.username) == 0:
            messages.error(request, "You are not a registered user")
            return False
        if len(request.POST["username"]) < 1:
            messages.error(request, "Username cannot be blank")
            isValid = False
        if len(request.POST["password"]) < 1:
            messages.error(request, "Password cannot be blank")
            isValid = False
        new_hash = bcrypt.hashpw(request.POST["password"].encode("utf-8"), user.pw_hashed.encode("utf-8"))
        if new_hash != user.pw_hashed:
            messages.error(request, "Password is incorrect")
            isValid = False
        if not isValid:
            return False

        request.session["logged_in"] = user.id

        return True

class User(models.Model):
    first_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    pw_hashed = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    usermanager = UserManager()