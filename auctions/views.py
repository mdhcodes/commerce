from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid
# Use Django to create the new listing form from the model.
from .forms import CreateListingForm, CreateBidForm

# Use Decimal() to convert the bid input by the user as a string to a decimal.
from decimal import Decimal


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
                # https://stackoverflow.com/questions/72062094/i-got-decimal-invalidoperation-class-decimal-conversionsyntax
                bid=Decimal(bid), 
                category=category,
                # image
                createdBy=user
                )        
        
        listing_data.save() 

        # Redirect to index.html
        # https://www.geeksforgeeks.org/django-modelform-create-form-from-models/
        # return HttpResponseRedirect(reverse("index"), {
        #     "message": "Your new listing was saved." # !!!!!! NOT WORKING - Listings were created but the message is not displayed. !!!!!!
        # })

        all_listings = Listing.objects.all()

        return render(request, "auctions/index.html", {
            "all_listings": all_listings,
            "new_listing_message": "Your new listing was saved."
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
    # form = CreateBidForm() # When this form is submitted, it also expects an argument to the add to/remove from watchlist path. Will hardcode form in HTML for now. # Error Message: NoReverseMatch at /bid/3 - Reverse for 'add_to_watchlist' with arguments '('',)' not found. 1 pattern(s) tried: ['add_to_watchlist/(?P<id>[0-9]+)\\Z']

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

    # The user who created (createdBy) the listing may “close” the auction from listing.html.
    # This makes the highest bidder the winner of the auction and makes the listing no longer active.
    # print("Listing Created By:", get_listing_data.createdBy) # Returns the user who created the listing.

    # Boolean check to find if the current user created this listing.
    creator = user_name == get_listing_data.createdBy 
    # print("Creator:", creator) # Returns True or False.

    # Check if Listing.is_open
    listing_is_open = get_listing_data.is_open

    # Get the last or highest bid and the user who placed it to determine the winner.
    highest_bid_amount = Listing.objects.values_list("bid", flat=True).get(pk=item_id)
    print("Highest Bid Amount:", highest_bid_amount)

    # Search Bid table for the item_id with the highest_bid and find the user who placed that bid.

    all_bids_for_item = Bid.objects.filter(listing_id=item_id)
    # print("All Bids for Item:", all_bids_for_item)

    # Get the bid that equals the highest bid.
    highest_bid = all_bids_for_item.get(bid=highest_bid_amount)
    print("Highest Bid:", highest_bid)

    # Get the user who placed the highest bid.
    highest_bidder_id = highest_bid.placedBy_id
    print("Highest Bidder ID:", highest_bidder_id)

    # user_with_highest_bid = Bid.objects.values_list("listing_id", flat=True).filter(bid=highest_bid) # Bid.objects.values_list("bid", flat=True).get(item_id=highest_bid)
    # print("User with Highest Bid:", user_with_highest_bid)
    # highest_bidder = user_with_highest_bid.values_list("placedBy_id", flat=True).values()
    # highest_bidder_id = user_with_highest_bid.values("placedBy")[0]["placedBy"]
    # print("Highest Bidder:", highest_bidder_id)
    
    context = {
        "listing_data": listing_data,
        "item_id": item_id,
        "user_is_watching": user_is_watching,
        "bid": last_bid,
        "total_bids": total_bids,
        "starting_bid": starting_bid,
        # "form": form
        "creator": creator,
        "listing_is_open": listing_is_open,
        "highest_bidder_id": highest_bidder_id
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

"""
NoReverseMatch at /bid/1
Reverse for 'add_to_watchlist' with arguments '('',)' not found. 1 pattern(s) tried: ['add_to_watchlist/(?P<id>[0-9]+)\\Z']
"auctions/listing.html" has two forms and when the user submits a bid the program throws an error because its expecting the argument for "add_to_watchlist" or "remove_from_watchlist".
"""

def bid(request, id):

    # https://stackoverflow.com/questions/59727384/multiple-django-forms-in-single-view-why-does-one-post-clear-other-forms
    # There are multiple forms on the listing page and both are being submitted when one button is clicked. Error is displayed requesting other form.

    listing_id = id
    user_name = request.user
    # user_id = request.user.id

    # https://stackoverflow.com/questions/866272/how-can-i-build-multiple-submit-buttons-django-form
    # Determine which form to use

    # If POST request and the arguments for add/remove from watchlist are empty OR select only the bid form OR prevent the add/remove from watchlist button
    if request.method == "POST": # and (not add_to_watchlist or not remove_from_watchlist):

        """
        # print("POST Data:", request.POST)
        # print("BID POST:", request.POST.get("placeBid")) # Returns user_bid

        # print("Request Body:", request.body)

        
        # <input type="submit" value="Place Bid"> - This HTML caused the following output with the key as '200' and the value as 'Place Bid'. QueryDict below:
        # request.POST = <QueryDict: {'csrfToken': ['djwi5iyo...'], 'bid': ['200', 'Place Bid'], 'listing': [''], 'placedBy': ['']}>
        # Changed to a button and received the following data: <QueryDict: {'csrfToken': ['djwi5iyo...'], 'bid': ['200'], 'listing': [''], 'placedBy': ['']}>
        
       
        # Store the user data in a variable called bid_amount.
        # bid_amount = CreateBidForm(request.POST) # NoReverseMatch at /bid/3 - Reverse for 'add_to_watchlist' with arguments '('',)' not found. 1 pattern(s) tried: ['add_to_watchlist/(?P<id>[0-9]+)\\Z']
        # The above code grabs the empty arguments from add to/remove from watchlist and wants to execute that route as well.

        # !!!!!! # When this form is submitted, it also expects an argument to the add to/remove from watchlist path. Will hardcode form in HTML for now. !!!!!!
        """        

        # print("POST Data:", request.POST) # Returns <QueryDict: {'csrfToken': ['djwi5iyo...'], 'placeBid': ['10']}> - Result from input field in HTML.
        # print("POST Data:", request.POST) # Returns <QueryDict: {'csrfToken': ['djwi5iyo...'], 'placeBid': ['10', 'user_bid']}> - Result with a button.

        # Error NoReverseMatch... 'add_to_watchlist' with arguments not found persists with hardcoded form. 
        
        """
        THE LOGIC TO PLACE A BID WORKS WITH THE DJANGO FORM AND THE HARDCODED FORM. THE DATABASES ARE UPDATED WHEN CONDITIONS ARE MET. HOWEVER, THE PROGRAM CRASHES BECAUSE IT
        IS ALSO EXPECTING AN ARGUMENT FOR THE ADD_TO/REMOVE_FROM_WATCHLIST PATH.
        """
        
        print("Request Body:", request.body) # Returns b'csrfToken=djwi5iyo...&placeBid=10&placeBid=user_bid' - Result with a button with value="user_bid".

        bid_amount = request.POST['placeBid']

        print("Bid Amount:", bid_amount)

        # Capture the bid_amount value.
        # current_bid = bid_amount["bid"].value() # Returns "Place Bid" not 200
        current_bid = Decimal(bid_amount)
        print("Current Bid:", current_bid) 
        
        last_bid = Listing.objects.values_list("bid", flat=True).get(pk=listing_id) # Returns bid for specified item or listing.
        print("Last Bid:", last_bid) 
        print("Type Last Bid:", type(last_bid)) # <class 'decimal.Decimal'>
        print("Type Current Bid:", type(current_bid)) # <class 'str'>

        # https://stackoverflow.com/questions/4643991/python-converting-string-into-decimal-number
        # If last bid is >= current bid stored in Listing table
        # if last_bid < Decimal(current_bid): # InvalidOperation at /bid/3 - [<class 'decimal.ConversionSyntax'>] bid must be saved as Decimal(bid) from the user
        if last_bid < current_bid:
            # Capture listing object with the listing_id from Listing table to save and update Listing and Bid tables.
            # listing = Listing.objects.filter(pk=listing_id) # ValueError at /bid/2 - Cannot assign "<QuerySet [<Listing: Platter 1 / Art>]>": "Bid.listing" must be a "Listing" instance.
            # listing = Listing.objects.get(pk=listing_id) # # Cannot assign "2": "Bid.listing" must be a "Listing" instance. # IntegrityError at /bid/2 - NOT NULL constraint failed: auctions_bid.listing_id # IntegrityError at /bid/2 - NOT NULL constraint failed: auctions_listing.createdBy_id
            listing = Listing.objects.filter(pk=listing_id).get(id=listing_id)
            print("Listing:", listing)

            # Save the Bid.
            # Save bid, listing_id, and user_name
            bid_data = Bid(
                # https://stackoverflow.com/questions/72062094/i-got-decimal-invalidoperation-class-decimal-conversionsyntax
                # bid=Decimal(current_bid),
                bid=current_bid, 
                listing=listing,
                placedBy=user_name
            )

            bid_data.save()   

            # THE FOLLOWING ERRORS WERE TELLING ME THAT I WAS NOT ACCESSING A SPECIFIC FIELD IN THE TABLE TO UPDATE. CORRECTION BELOW WITH update_listing.
            # listing=listing, # Cannot assign "2": "Bid.listing" must be a "Listing" instance. # IntegrityError at /bid/2 - NOT NULL constraint failed: auctions_bid.listing_id # IntegrityError at /bid/2 - NOT NULL constraint failed: auctions_listing.createdBy_id
            # listing=listing_id, # ValueError at /bid/2 - Cannot assign "2": "Bid.listing" must be a "Listing" instance.

            # Update the Listing bid / current bid.
            # https://stackoverflow.com/questions/3681627/how-to-update-fields-in-a-model-without-creating-a-new-record-in-django
            update_listing = Listing.objects.get(pk=listing_id)
            # https://stackoverflow.com/questions/72062094/i-got-decimal-invalidoperation-class-decimal-conversionsyntax
            # update_listing.bid = Decimal(current_bid)
            update_listing.bid = current_bid

            # update_listing = Listing(
            #     bid=current_bid
            #     # IntegrityError at /bid/2 - NOT NULL constraint failed: auctions_listing.createdBy_id
            # )

            update_listing.save()

            listing_data = Listing.objects.filter(pk=listing_id)
            
            return render(request, "auctions/listing.html", {
                "listing data": listing_data,
                "bid_success_message": "Bid was successful.", # Going to route /bid/5 but there's no bid.html????????
                "bid_placed": True
            }) 

            """
            # https://stackoverflow.com/questions/75338256/is-there-a-way-to-add-context-to-django-reverse-function
            # "reverse() only produces a string: a path."
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)), {
                "listing data": listing_data,
                "bid_success_message": "Bid was successful." # No message displayed.
            })
            """

        else:

            listing_data = Listing.objects.filter(pk=listing_id)

            return render(request, "auctions/listing.html", {
                "listing data": listing_data,
                # To display the message below, check on the server with a try / except.
                "bid_error_message": "Bid error: Your bid was invalid or it must be greater than the starting or current bid.", # ValueError at /bid/3 - invalid literal for int() with base 10: '-0.03'
                "bid_placed": False
            }) 

            """
            # https://stackoverflow.com/questions/75338256/is-there-a-way-to-add-context-to-django-reverse-function
            # "reverse() only produces a string: a path."
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)), {
                "listing data": listing_data,
                # To display the message below, check on the server with a try / except.
                "bid_error_message": "Bid error: Your bid was invalid or it must be greater than the starting or current bid." # No message displayed.
            })
            """
        
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


"""
The user who created (createdBy) the listing may “close” the auction from listing.html.
This makes the highest bidder the winner of the auction and makes the listing no longer active.
"""

def close(request, id):

    # Get item id
    item_id = id

    # Get user
    user_name = request.user

    # Auction is closed when Listing.is_open == False
    # Get listing data
    get_listing_data = Listing.objects.get(pk=id)
    get_listing_data.is_open = False
    # Save status to Listing database.
    get_listing_data.save()

    listing_data = Listing.objects.filter(pk=id)

    watchlist_data = get_listing_data.watchlist.all() 
    user_is_watching = user_name in watchlist_data

    # Get the current bid.
    last_bid = Listing.objects.values_list("bid", flat=True).get(pk=item_id)

    # Get total bids.
    total_bids = len(Bid.objects.filter(listing_id=item_id))

    # Get starting bid.
    starting_bid = True if total_bids == 0 else False

    # Get creator of this listing.
    creator = user_name == get_listing_data.createdBy 

    return render(request, "auctions/listing.html", {
        "listing_data": listing_data,
        "item_id": item_id,
        "user_is_watching": user_is_watching,
        "bid": last_bid,
        "total_bids": total_bids,
        "starting_bid": starting_bid,
        # "form": form
        "creator": creator,
        "close_message": "Congratulations! This auction is now closed."
    })


