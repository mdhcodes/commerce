# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#specifying-a-custom-user-model
# "If you’re starting a new project, it’s highly recommended to set up a custom user model, even if the default User model is sufficient for you." 
# "This model behaves identically to the default user model, but you’ll be able to customize it in the future if the need arises (AbstractUser)."

# Don’t forget to point AUTH_USER_MODEL to it in settings.py below DATABASES. Do this before creating any migrations or running manage.py migrate for the first time.
# AUTH_USER_MODEL = 'auctions.User'

# Also, register the model in the app’s admin.py.

from django.contrib.auth.models import AbstractUser
from django.db import models


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
    image = models.ImageField(upload_to="images/") # blank=True - field may be empty.    

    # https://stackoverflow.com/questions/1139393/what-is-the-best-django-model-field-to-use-to-represent-a-us-dollar-amount
    # https://dev.to/koladev/django-tip-use-decimalfield-for-money-3f63
    # https://www.geeksforgeeks.org/decimalfield-django-models/
    bid = models.DecimalField(max_digits=19, decimal_places=2, default=00.00) # "Stores numbers up to one billion with a resolution of 4 decimal places."

    # A watchlist for each listing that holds all the users watching it. 
    watchList = models.ManyToManyField(User, blank=True, related_name="user") # blank=True means a Listing can have no users watching it.
    
    # https://www.geeksforgeeks.org/python-relational-fields-in-django-models/?ref=gcse
    # "It is a good practice to name the many-to-one field with the same name as the related model, lowercase."
    # "Many-to-one relations are defined using ForeignKey field of django.db.models." A user can have multiple listings but a listing can't have multipls users.
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE) # If a user is deleted, all listings posted by that user are deleted as well. 

    # Instructions to convert Listing object into a string.
    # https://cs50.harvard.edu/web/2020/notes/4/#shell
    def __str__(self):
        return f"{self.title} / {self.category}"