from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing
# Use Django to create the new listing form from the model.
from .forms import CreateListingForm


def index(request):

    """
    Active Listings: 
    The default/index route should allow users to view all of the currently active auction listings. 
    For each active listing, the page will display the title, description, current price, and photo (if one exists for the listing).
    """

    all_listings = Listing.objects.all()

    context = {
       "all_listings": all_listings
    }
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


"""
Create Listing: Users may create a new listing. 
They will be able to enter the listing title, description, category, image, and starting bid. 
Users should also optionally be able to provide a URL for an image for the listing.
"""

def new_listing(request):
    
    title = "Create Listing"

    # POST request
    if request.method == "POST":
        # Store the user data in a variable called listing_data.
        # Image data will be stored in the request.FILES object.
        # https://docs.djangoproject.com/en/5.0/ref/forms/api/#binding-uploaded-files-to-a-form
        listing_data = CreateListingForm(request.POST, request.FILES)

        # Get user from the POST request.
        user_name = request.user
     
        # Capture the new listing_data form values.
        title = listing_data["title"].value()
        description = listing_data["description"].value()
        bid = listing_data["bid"].value()
        category = listing_data["category"].value()
        # image
        user = user_name

        # Save the listing_data form values to the auctions database.
        # https://docs.djangoproject.com/en/5.0/topics/db/queries/
        # https://docs.djangoproject.com/en/5.0/ref/models/instances/#saving-objects
        # https://docs.djangoproject.com/en/5.0/ref/models/instances/#how-django-knows-to-update-vs-insert
        listing_data = Listing(title=title, 
                description=description, 
                bid=bid, 
                category=category,
                # image
                createdBy=user
                )        
        
        listing_data.save() 

        # Redirect to index.html
        # https://www.geeksforgeeks.org/django-modelform-create-form-from-models/
        return HttpResponseRedirect(reverse("index"), {
            "message": "Your new listing was saved." # !!!!!! NOT WORKING - Listings were created but the message is not displayed. !!!!!!
        })
             
    else:
        # GET request
        return render(request, "auctions/new_listing.html", {
            "title": title,
            "form": CreateListingForm()
        })