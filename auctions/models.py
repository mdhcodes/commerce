# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#specifying-a-custom-user-model
# "If you’re starting a new project, it’s highly recommended to set up a custom user model, even if the default User model is sufficient for you." 
# "This model behaves identically to the default user model, but you’ll be able to customize it in the future if the need arises (AbstractUser)."

# Don’t forget to point AUTH_USER_MODEL to it in settings.py below DATABASES. Do this before creating any migrations or running manage.py migrate for the first time.
# AUTH_USER_MODEL = 'auctions.User'

# Also, register the model in the app’s admin.py.

from django.contrib.auth.models import AbstractUser
from django.db import models

# Validate numbers are within a certain range with MinValueValidator and MaxValueValidator.
# https://stackoverflow.com/questions/44022056/validators-minvaluevalidator-does-not-work-in-django
from django.core.validators import MinValueValidator
# Import Decimal to set the value of MinValueValidator.
from decimal import Decimal


class User(AbstractUser):
    pass # Pass = placeholder for future code. Python will do nothing when it sees the 'pass' statement.


# Auction Listing
class Listing(models.Model):
    # https://docs.djangoproject.com/en/5.0/ref/databases/#character-fields (max_length restricted to 255 characters if you are using unique=True for the field)
    title = models.CharField(max_length=100)
    
    # https://docs.djangoproject.com/en/5.0/ref/models/fields/#textfield
    description = models.TextField()
    
    category = models.CharField(max_length=100, blank=True) # blank=True - field may be empty.)

    # https://docs.djangoproject.com/en/5.0/ref/models/fields/#imagefield
    # https://docs.djangoproject.com/en/5.0/ref/forms/fields/#imagefield
    # https://docs.djangoproject.com/en/5.0/ref/forms/api/#binding-uploaded-files
    # ImageField requires the Pillow library. # https://pillow.readthedocs.io/en/latest/installation/basic-installation.html
    # https://www.geeksforgeeks.org/imagefield-django-models/
    # image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    image = models.ImageField(upload_to="images/") #, null=True, blank=True) # blank=True - field may be empty. # Image files are uploaded to the media/images directory through the admin account. However, image files are not uploaded (to this directory) from the user.

    # https://cs50.harvard.edu/web/2020/projects/2/commerce/#specification
    # CS50 specifications indicate that "users should also optionally be able to provide a URL for an image for the listing.


    # https://stackoverflow.com/questions/1139393/what-is-the-best-django-model-field-to-use-to-represent-a-us-dollar-amount
    # https://dev.to/koladev/django-tip-use-decimalfield-for-money-3f63
    # https://www.geeksforgeeks.org/decimalfield-django-models/
    # https://stackoverflow.com/questions/12384460/allow-only-positive-decimal-numbers # Ensure bids are never negative numbers with MinValueValidator.
    bid = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]) #, default=00.00) # "Stores numbers up to one billion with a resolution of 4 decimal places."

    # https://docs.djangoproject.com/en/5.0/ref/models/fields/#django.db.models.ForeignKey.related_name
    # The name to use for the relation from the related object back to this one. It’s also the default value for related_query_name (the name to use for the reverse filter name from the target model).
    # https://stackoverflow.com/questions/2642613/what-is-related-name-used-for
    # https://cs50.harvard.edu/web/2020/notes/4/#shell
    
    # Each listing has a watchlist that includes all the users who are watching it or have added it to their watchlist. One listing may be on many user watchlists.
    watchlist = models.ManyToManyField(User, blank=True, related_name="watch_list") # blank=True means a Listing can have no users watching it.

    # Each listing needs to be open to bids or closed to bids. 
    is_open = models.BooleanField(default=True)
    
    # https://www.geeksforgeeks.org/python-relational-fields-in-django-models/?ref=gcse
    # "It is a good practice to name the many-to-one field with the same name as the related model, lowercase."
    # "Many-to-one relations are defined using ForeignKey field of django.db.models." A user can have multiple listings but a listing can't have multipls users.
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user") # If a user is deleted, all listings posted by that user are deleted as well. 

    # Instructions to convert Listing object into a string.
    # https://cs50.harvard.edu/web/2020/notes/4/#shell
    def __str__(self):
        return f"{self.title} / {self.category}"
    


class Bid(models.Model):
    # https://stackoverflow.com/questions/1139393/what-is-the-best-django-model-field-to-use-to-represent-a-us-dollar-amount
    # https://dev.to/koladev/django-tip-use-decimalfield-for-money-3f63
    # https://www.geeksforgeeks.org/decimalfield-django-models/
    # https://stackoverflow.com/questions/70738255/whats-the-default-value-for-a-decimalfield-in-django
    # https://stackoverflow.com/questions/12384460/allow-only-positive-decimal-numbers # Ensure bids are never negative numbers with MinValueValidator.
    bid = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]) #, default=00.00) # "Stores numbers up to one billion with a resolution of 10 decimal places."
 
    # Error for new listings when listing.html is requested - Bid matching query does not exist. The Listing and Bid table bid field are not connected. No bid has been placed yet but the program is looking for that information.
    # bid = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    # https://www.geeksforgeeks.org/python-relational-fields-in-django-models/?ref=gcse
    # Listing is a many-to-one relationship.
    # A listing can have multiple bids but a bid can't have multiple listings. If a listing is deleted, all bids posted for that listing are deleted as well.
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    # User is a many-to-one relationship.
    # A user can have multiple bids but a bid can't have multiple users. If a user is deleted, all bids posted by that user are deleted as well. 
    placedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids") # If a user is deleted, all bids posted by that user are deleted as well. 

    
    def __str__(self):
        return f"{self.id} / {self.listing} / {self.bid}"


class Comment(models.Model):
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comment")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")

    def __str__(self):
        return f"{self.author} / {self.listing}"