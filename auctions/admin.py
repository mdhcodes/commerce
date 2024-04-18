from django.contrib import admin

# Register your models here.
# https://cs50.harvard.edu/web/2020/notes/4/#django-admin
# Let Django know which models to access in the admin app.
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
# Also, register the model in the app’s admin.py:

from django.contrib.auth.admin import UserAdmin
from .models import User, Listing, Bid, Comment

# https://cs50.harvard.edu/web/2020/notes/4/#django-admin
# To customize the admin app interface, create a new class here.
# Visit the admin page by going to http://127.0.0.1:8000/admin

# To begin using this tool, create an administrative user:

# \command\path> python manage.py createsuperuser
# Username: user_a
# Email address: a@a.com
# Password:
# Password (again):
# Superuser created successfully.

# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#modeladmin-objects
class UserAdmin(admin.ModelAdmin):
    pass

class ListingAdmin(admin.ModelAdmin):
    pass

class BidAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass


# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
# Also, register the (User) model in the app’s admin.py.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
