from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Category, Comment
from .forms import CreateListingForm, BidSubmitForm, CommentSubmitForm
from .helpers import get_item

# INDEX page with active listings
def index(request):
    listings = Listing.objects.filter(active=True)
    current_prices = {}

    for listing in listings:
        try:
            current_prices[listing.id] = Bid.objects.filter(listing=listing).order_by("-price").first().price
        except: 
            current_prices[listing.id] = listing.price

    return render(request, "auctions/index.html", {
        "listings": listings,
        "prices": current_prices
    })

# LOGIN page
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/login.html")

# REGISTER page
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

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
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/register.html")

# LOGOUT and redirect to INDEX
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# LISTING page
def show_listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except:
        return render(request, "auctions/error.html", {"message": "Listing not found."})

    bids = Bid.objects.filter(listing=listing_id).order_by("-price")
    comments = Comment.objects.filter(listing=listing_id).order_by("-date")

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid_form": BidSubmitForm(),
        "bids": bids,
        "comment_form": CommentSubmitForm(),
        "comments": comments
    })

# CREATE listing
@login_required
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = User.objects.get(id=request.user.id)
            listing.save()
            return HttpResponseRedirect(reverse("show_listing", args=[listing.id]))
        else:
            return render(request, "auctions/error.html", {"message": "Listing not created. Try again."})
    else:
        return render(request, "auctions/create.html", {
            "form": CreateListingForm()
        })

# CLOSE listing
@login_required
def close_listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except:
        return render(request, "auctions/error.html", {"message": "Listing not found."})

    if request.user == listing.owner and listing.active:
        listing.active = False
        try:
            highest = Bid.objects.filter(listing=listing_id).order_by("-price").first()
        except:
            return render(request, "auctions/error.html", {"message": "Couldn't close the listing."})
        else:
            listing.winner = highest.user if highest else None
            listing.save()
            return HttpResponseRedirect(reverse("show_listing", args=[listing.id])) 
    else:
        return render(request, "auctions/error.html", {"message": "Couldn't close the listing."})

# BID on listing
@login_required
def bid_submit(request, listing_id):
    if request.method == "POST":
        form = BidSubmitForm(request.POST)
        try:
            listing = Listing.objects.get(id=listing_id)
        except:
            return render(request, "auctions/error.html", {"message": "Listing not found."})

        try:
            highest = Bid.objects.filter(listing=listing_id).order_by("-price").first().price 
        except:
            highest = 0
        
        if form.is_valid() and listing.active:
            if float(request.POST["price"]) > highest and float(request.POST["price"]) >= listing.price:
                bid = form.save(commit=False)
                bid.user = User.objects.get(id=request.user.id)
                bid.listing = Listing.objects.get(id=listing_id)
                bid.save()
                listing.users_watching.add(bid.user)
                return HttpResponseRedirect(reverse("show_listing", args=[listing.id]))
            else:
                return render(request, "auctions/error.html", {"message": "Bid not submitted. Try again."})
        else:
            return render(request, "auctions/error.html", {"message": "Bid not submitted. Try again."})

    else:
        return HttpResponseRedirect(reverse("index"))

# Add COMMENT on listing
@login_required
def comment(request, listing_id):
    if request.method == "POST":
        form = CommentSubmitForm(request.POST)
        try:
            listing = Listing.objects.get(id=listing_id)
        except:
            return render(request, "auctions/error.html", {"message": "Listing not found."})
        
        if form.is_valid() and listing.active:
            comment = form.save(commit=False)
            comment.user = User.objects.get(id=request.user.id)
            comment.listing = Listing.objects.get(id=listing_id)
            comment.save()
            return HttpResponseRedirect(reverse("show_listing", args=[listing.id]))
        else:
            return render(request, "auctions/error.html", {"message": "Comment not submitted. Try again."})
    else:
        return HttpResponseRedirect(reverse("index"))

# Add listing to WATCHLIST
@login_required
def watchlist(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except:
        return render(request, "auctions/error.html", {"message": "Listing not found."})
    
    user = User.objects.get(id=request.user.id)
    if listing in user.watchlisted.all():
        listing.users_watching.remove(user)
    else:
        listing.users_watching.add(user)
    return HttpResponseRedirect(reverse("show_listing", args=[listing.id]))

# Show user's WATCHLIST
@login_required
def show_watchlisted(request):
    user = User.objects.get(id=request.user.id)
    listings = user.watchlisted.all()
    current_prices = {}

    for listing in listings:
        try:
            current_prices[listing.id] = Bid.objects.filter(listing=listing).order_by("-price").first().price
        except: 
            current_prices[listing.id] = listing.price

    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "prices": current_prices
    })

# Show list of CATEGORIES
def show_categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

# Show active listings from selected CATEGORY
def show_category(request, name):
    try:
        category = Category.objects.get(name=name)
    except:
        return render(request, "auctions/error.html", {"message": "Category not found."})

    listings = Listing.objects.filter(category=category).filter(active=True)
    current_prices = {}

    for listing in listings:
        try:
            current_prices[listing.id] = Bid.objects.filter(listing=listing).order_by("-price").first().price
        except: 
            current_prices[listing.id] = listing.price

    return render(request, "auctions/category.html", {
        "listings": listings,
        "category": category,
        "prices": current_prices
    })
