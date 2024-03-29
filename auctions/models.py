# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
# "If you’re starting a new project, it’s highly recommended to set up a custom user model, even if the default User model is sufficient for you." 
# "This model behaves identically to the default user model, but you’ll be able to customize it in the future if the need arises (AbstractUser)."

# Don’t forget to point AUTH_USER_MODEL to it in settings.py below DATABASES. Do this before creating any migrations or running manage.py migrate for the first time.
# AUTH_USER_MODEL = 'auctions.User'

# Also, register the model in the app’s admin.py.

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass # Pass = placeholder for future code. Python will do nothing when it sees the 'pass' statement.


# Auction Listings
class Listings(models.Model):
    pass
    # title
    # image
    # description
    # category
    # bid / price (foreign key)
    # place bid button
    # add to watchlist
    # details
    #     seller
    #     condition (new or used)



# User Bids
class Bids(models.Model):
    pass
    # bid dollar amount
    # item id (foreign key)
    # user id (foreign key)


# Comments (on listings)
class Comments(models.Model):
    pass
    # comment
    # item id (foreign key)
    # user id (foreign key)
