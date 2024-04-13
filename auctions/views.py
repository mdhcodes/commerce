from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid
# Use Django to create the new listing form from the model.
from .forms import CreateListingForm, CreateBidForm


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
        # https://pylessons.com/django-images # REVIEW THIS TUTORIAL!!!!!
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
    

"""
Listing Page: Clicking on a listing should take users to a page specific to that listing. 
On that page, users should be able to view all details about the listing, including the current price for the listing.
"""

def listing(request, id):
    
    item_id = id
    # print("Item id:", item_id) # Returns ID
    # print("ID Type", type(item_id)) # <class 'int'>

    # Retrieve a specific row in the database table Listings.
    # https://www.w3schools.com/django/django_queryset_get.php
    listing_data = Listing.objects.filter(pk=item_id) #.values() # Returns iterable QuerySet with or without .values()
    # listing_data = Listing.objects.get(pk=item_id) # Returns Platter 1 / Art - .get() retrieves a single object - Listing object is not iterable
    # If I wanted to use the above .get() I'd have to place listing_data in the context and access each in the html as listing_data.title, listing_data.description, listing_data.description.bid, etc. without a 'for loop'.
    # print("Listing Data:", listing_data) # Returns QuerySet
    
    # Watchlist Database Queries
    # Does the user have this item on their watch_list?
    # Get user
    user_name = request.user
    # print("User Name:", user_name) # Returns user's name
    # user_id = request.user.id
    # print("User ID:", user_id) # Returns user's ID

    # https://stackoverflow.com/questions/4319469/queryset-object-has-no-attribute-error-trying-to-get-related-data-on-manytoma
    get_listing_data = Listing.objects.get(pk=item_id) # Retrieves a single Listing object - Returns title / category
    # print("Get Listing Data:", get_listing_data)
    watchlist_data = get_listing_data.watchlist.all() # Returns QuerySet of users linked to the listing's watchlist.
    # print("Watchlist Data:", watchlist_data)
   
    # user_is_watching = False
    user_is_watching = user_name in watchlist_data

    # Add Bid form if the user is signed in.
    form = CreateBidForm()

    # Get the current bid.
    # https://stackoverflow.com/questions/25881015/django-queryset-return-single-value
    # https://docs.djangoproject.com/en/5.0/ref/models/querysets/#values-list
    # bid_data = Listing.objects.values_list("bid", flat=True) # Returns all bids
    last_bid = Listing.objects.values_list("bid", flat=True).get(pk=item_id) # Returns bid for specified item or listing.
    # print("Bid Data:", bid_data)
         
    # Show number of bids on the front end.
    # ??!!!!!! I need total_bids fro specific listing!!!!!!??
    # total_bids = len(Bid.objects.values_list("bid", flat=True)) # All listing bids in Bid table. 
    total_bids = len(Bid.objects.filter(listing_id=item_id)) # All bids on one listing.
    # print("Total Bids:", total_bids)

    # If the total number of bids == 0:
    # https://stackoverflow.com/questions/394809/does-python-have-a-ternary-conditional-operator
    # a if condition else b
    starting_bid = True if total_bids == 0 else False
    # if total_bids == 0:
        # starting_bid = True # HTML should read Starting Bid:

    context = {
        "listing_data": listing_data,
        "item_id": item_id,
        "user_is_watching": user_is_watching,
        "bid": last_bid,
        "total_bids": total_bids,
        "starting_bid": starting_bid,
        "form": form
    }
    
    return render(request, "auctions/listing.html", context)


"""
Watchlist - Add/Remove Items
If the user is signed in, the may add the item to their “Watchlist.” 
If the item is already on the watchlist, they may remove it.
"""

def add_to_watchlist(request, id):

    listing_id = id
    user_name = request.user

    # https://docs.djangoproject.com/en/5.0/topics/db/queries/#saving-foreignkey-and-manytomanyfield-fields
    # Saving ForeignKey and ManyToManyField fields
    # Get listing
    get_listing_data = Listing.objects.get(pk=listing_id)

    # If POST request
    if request.method == "POST":

        # Update ManyToManyField using add(). Add user to the watchlist in the Listing table for the specified item.
        get_listing_data.watchlist.add(user_name)
        
        # Redirect to listing.html passing the argument 'id' for the listing.
        # https://stackoverflow.com/questions/52575418/reverse-with-prefix-argument-after-must-be-an-iterable-not-int
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def remove_from_watchlist(request, id):

    listing_id = id
    user_name = request.user  

    # https://docs.djangoproject.com/en/5.0/topics/db/queries/#many-to-many-relationships
    # Remove items from a field in the database
    # Get listing
    get_listing_data = Listing.objects.get(pk=listing_id)

    # If POST request
    if request.method == "POST":        

        # Update ManyToManyField using remove(). Remove the user from the watchlist in the Listing table for the specified item.
        get_listing_data.watchlist.remove(user_name)
        
        # Redirect to listing.html passing the argument 'id' for the listing
        # https://stackoverflow.com/questions/52575418/reverse-with-prefix-argument-after-must-be-an-iterable-not-int
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    

"""
Watchlist Page: Authenticated users may access a Watchlist page, which displays all of the listings on their watchlist. 
Clicking on any of the listings takes the user to that listing’s page.
"""

def watchList(request):
    user_name = request.user

    # https://docs.djangoproject.com/en/5.0/topics/db/queries/#following-relationships-backward
    # https://stackoverflow.com/questions/2642613/what-is-related-name-used-for
    # Get all listings / watchlists for the current user
    get_user_watchList = user_name.watch_list.all()
    print("Get User WatchList", get_user_watchList)

    context = {
        "watchList": get_user_watchList
    }

    return render(request, "auctions/watchlist.html", context)


"""
Bid - An authenticated user may bid on an item.
The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). 
If the bid doesn’t meet those criteria, the user should be presented with an error.
"""

def bid(request, id):

    listing_id = id
    user_name = request.user
    # user_id = request.user.id

    # If POST request
    if request.method == "POST":

        # Store the user data in a variable called bid_amount.
        bid_amount = CreateBidForm(request.POST)
        print("Bid Amount:", bid_amount)

        # Capture the bid_amount value.
        current_bid = bid_amount["bid"].value()
        print("Current Bid:", current_bid)  
        
        # last_bid = Listing.objects.values_list("bid", flat=True).get(pk=listing_id) # Returns bid for specified item or listing.
        
        # Capture listing object with the listing_id from Listing table to save and update Listing and Bid tables.
        # listing = Listing.objects.filter(pk=listing_id) # ValueError at /bid/2 - Cannot assign "<QuerySet [<Listing: Platter 1 / Art>]>": "Bid.listing" must be a "Listing" instance.
        listing = Listing.objects.get(pk=listing_id)
        # print("Listing:", listing)

        # Save the Bid.
        # Save bid, listing_id, and user_name
        bid_data = Bid(
            bid=current_bid, 
            listing=listing,
            # listing=listing, # Cannot assign "2": "Bid.listing" must be a "Listing" instance. # IntegrityError at /bid/2 - NOT NULL constraint failed: auctions_bid.listing_id # IntegrityError at /bid/2 - NOT NULL constraint failed: auctions_listing.createdBy_id
            # listing=listing_id, # ValueError at /bid/2 - Cannot assign "2": "Bid.listing" must be a "Listing" instance.
            placedBy=user_name
        )

        bid_data.save()   

        # Update the Listing bid / current bid.
        update_listing = Listing(
            bid=current_bid
            # IntegrityError at /bid/2 - NOT NULL constraint failed: auctions_listing.createdBy_id
        )

        update_listing.save()
        
    # Redirect to listing.html
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

"""
def bid(request, id):

    listing_id = id
    user_name = request.user
    # user_id = request.user.id

    # If POST request
    if request.method == "POST":  

        # Store the user data in a variable called bid_amount.
        bid_amount = CreateBidForm(request.POST)
        print("Bid Amount:", bid_amount)

        # Capture the bid_amount value.
        current_bid = bid_amount["bid"].value()
        print("Current Bid:", current_bid)  
        
        last_bid = Listing.objects.values_list("bid", flat=True).get(pk=listing_id) # Returns bid for specified item or listing.
        # If last bid is >= current bid stored in Listing table
        if last_bid >= int(current_bid):

            # Capture listing object with the listing_id from Listing table to save and update Listing and Bid tables.
            # listing = Listing.objects.filter(pk=listing_id) # ValueError at /bid/2 - Cannot assign "<QuerySet [<Listing: Platter 1 / Art>]>": "Bid.listing" must be a "Listing" instance.
            listing = Listing.objects.get(pk=listing_id)
            # print("Listing:", listing)

            # Save the Bid.
            # Save bid, listing_id, and user_name
            bid_data = Bid(
                bid=current_bid,
                listing=listing,
                # listing=listing_id, # Cannot assign "2": "Bid.listing" must be a "Listing" instance. # IntegrityError at /bid/2 - NOT NULL constraint failed: auctions_bid.listing_id
                placedBy=user_name
            )

            bid_data.save()   

            # Update the Listing bid / current bid.
            update_listing = Listing(
                bid=current_bid
            )

            update_listing.save()

        else:
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)), {
                "message": "Bid error: Your bid must be greater than the starting or current bid."
            })        
    
    # Redirect to listing.html
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


"""
