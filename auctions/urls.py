from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # Add path to create a new listing.
    path("new_listing", views.new_listing, name="new_listing"),
    # Add path to listing page.
    path("listing/<int:id>", views.listing, name="listing"),
    # Add path to add an item/listing to the user's Watchlist
    path("add_to_watchlist/<int:id>", views.add_to_watchlist, name="add_to_watchlist"),
    # Add path to remove an item/listing from the user's Watchlist
    path("remove_from_watchlist/<int:id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    # Add path to watchlist page.
    path("watchList", views.watchList, name="watchList"),
    # Add path to place a bid.
    path("bid/<int:id>", views.bid, name="bid")
]
