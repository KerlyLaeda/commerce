from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="new_listing"),
    path("details/<str:pk>", views.listing_details, name="listing_details"),
    # in network project got the same issue when posts were not displayed, fixed by adding separate url for addin new post
    path("details/<str:pk>", views.add_comment, name="add_comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<str:pk>", views.toggle_watchlist, name="toggle_watchlist"),
    path("categories", views.all_categories, name="all_categories"),
    path("categories/<str:category>", views.items_in_category, name="items_in_category"),
]
