from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt

# User Manager for methods to query the DB
class UserManager(models.Manager):
    # The register method that validates and created new users
    def register(self, request):
        # Validation starts here using a flag, isValid, to check to make sure the first name field is not blank and is all letters,
        # to check that the username field is not blank, to make sure that the user is not already registered, and to make sure the passwords entered match
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

        # If the registration passes validation, the password is hashed using bcrypt
        hashed_pw = bcrypt.hashpw(request.POST["password"].encode("utf-8"), bcrypt.gensalt())
        # The user is then created and saved to the DB
        new_user = User (
                first_name = request.POST["first_name"],
                username = request.POST["username"],
                pw_hashed = hashed_pw,
            )
        new_user.save()

        # The user's ID is stored in session for a logged in status
        request.session["logged_in"] = new_user.id

        return True

    # The login method validates and logs in existing users
    def login(self, request):
        # Validation starts here using a flag, isValid, to check to make sure the username field is not blank,
        # the user is registered and exists in the DB, to check that the password field is not blank
        isValid = True
        if len(request.POST["username"]) < 1:
            messages.error(request, "Username cannot be blank")
            return False
        user = User.objects.filter(username=request.POST["username"])
        if len(user) == 0:
            messages.error(request, "You are not a registered user")
            return False
        if len(request.POST["password"]) < 1:
            messages.error(request, "Password cannot be blank")
            isValid = False
        # If the user validation is succesful, the user is pulled from the DB by username
        user = User.objects.get(username=request.POST["username"])
        # The password is then validated by hashing the entered password with bcrypt and comparing it to the hased password stored in the DB
        new_hash = bcrypt.hashpw(request.POST["password"].encode("utf-8"), user.pw_hashed.encode("utf-8"))
        if new_hash != user.pw_hashed:
            messages.error(request, "Password is incorrect")
            isValid = False
        if not isValid:
            return False

        # If all of the validation passes, the user is logged in
        request.session["logged_in"] = user.id

        return True

# The model for users, has the user_manager for the methods to query the DB
class User(models.Model):
    first_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    pw_hashed = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    user_manager = UserManager()
