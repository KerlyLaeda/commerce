from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import NewListingForm, NewCommentForm
from .models import User, AuctionListing, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all()
    })


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


# Listing views
@login_required
def new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():

            # Create an instance of AuctionListing from the form data
            new_listing = form.save(commit=False)

            # Set the owner to the current logged-in user
            new_listing.owner = request.user

            # Save the modified instance with the owner set
            new_listing.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/new_listing.html", {
                "form": form
            })

    return render(request, "auctions/new_listing.html", {
        "form": NewListingForm
    })


def listing_details(request, pk):
    listing = AuctionListing.objects.get(id=pk)
    comments = Comment.objects.filter(listing=listing).order_by("-date_posted")
    comment_form = NewCommentForm()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "comment_form": comment_form
    })


@login_required
def place_bid(request):
    """ If the user is signed in, the user should be able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user should be presented with an error. """
    starting_bid = AuctionListing.objects.get()
    max_bid = AuctionListing.objects.get()

    if request.method == "POST":
        return render(request, "auctions/listing.html", {

        })

    # user_bid >= starting & > max
    # message = ""
    # if user_bid <= max_bid:
    #     message = "Bid made successfully."
    # message = "The bid must be greater than the current bid."


@login_required
def close_listing():
    pass


@login_required
def add_comment(request, pk):
    listing = AuctionListing.objects.get(id=pk)

    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.listing = listing
            comment.save()
            return redirect("listing_detail", id=pk)
    else:
        form = NewCommentForm()

    return render(request, "add_comment.html", {"form": form})
    # listing = AuctionListing.objects.get(id=pk)
    #
    # text = request.POST.get("new_comment")
    # new_comment = Comment(
    #     author=request.user,
    #     text=text,
    #     listing=listing
    # )
    #
    # new_comment.save()
    #
    # # Redirect to the same page
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    #form is not displayed (???) {{form.as_p}}
    # listing = AuctionListing.objects.get(id=pk)
    # new_comment = None
    # if request.method == "POST":
    #     form = NewListingForm(request.POST)
    #     if form.is_valid():
    #         new_comment = form.save(commit=False)
    #         new_comment.author = request.user
    #         new_comment.save()
    #
    #         return HttpResponseRedirect(reverse("index"))
    #     else:
    #         form = NewCommentForm()
    #     return render(request, "auctions/listing.html", {
    #         'listing': listing,
    #         'new_comment': new_comment,
    #         'form': form
    #     })


@login_required
def toggle_watchlist(request, pk):
    """ Add to and remove from watchlist """

    listing = AuctionListing.objects.get(id=pk)

    # If an item is not in the watchlist, add it, otherwise remove it
    if listing:
        listing.in_watchlist = not listing.in_watchlist
        listing.save()

        # Redirect to the same page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def watchlist(request):
    """ Display the listings that are currently in the user's watchlist """

    user_watchlist = AuctionListing.objects.filter(owner=request.user, in_watchlist=True)

    return render(request, "auctions/watchlist.html", {
        "user_watchlist": user_watchlist
    })


def all_categories(request):
    """ Display a page with all listing categories """

    # Retrieve all categories
    categories = [choice[0] for choice in AuctionListing.AuctionCategory.choices]

    return render(request, "auctions/all_categories.html", {
        "categories": categories
    })


def items_in_category(request, category):
    """ Display all active listings in a chosen category """

    category_listings = AuctionListing.objects.filter(category=category)

    return render(request, "auctions/category.html", {
        "category": category,
        "category_listings": category_listings
    })
