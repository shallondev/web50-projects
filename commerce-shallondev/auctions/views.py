from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from .forms import BidForm, CategoryFilterForm, CloseAuctionForm, CommentForm, CreateListingForm, WatchListForm

from .models import Bid, Comments, Listing, User, WatchList


@login_required
def create_listing(request):
    """
    Create new listings of items
    """
    if request.method == "POST":
        # If form is valid save it to the database
        form = CreateListingForm(request.POST)
        category_form = CategoryFilterForm(request.POST)

        if form.is_valid() and category_form.is_valid():
            form.instance.created_by = request.user
            new_listing = form.save()

            # Associate the listing with the selected category
            selected_category = category_form.cleaned_data['category']
            if selected_category:
                new_listing.categories.add(selected_category)

            # Create a Bid instance for the newly created listing with no user
            Bid.objects.create(listing=new_listing, amount=form.cleaned_data['price'], user=None)
            return HttpResponseRedirect(reverse("index"))

    else:
        form = CreateListingForm()
        category_form = CategoryFilterForm()

    return render(request, "auctions/create_listing.html", {
        'form': form,
        'category_form': category_form,
    })


def index(request):
    # Get active listings.
    listings = Listing.objects.filter(is_active=True)

    return render(request, "auctions/index.html", {
        "listings" : listings
    })


def listing_page(request, listing_title):
    """
    Show details about the listing
    Allow ability to add listing to users watchlist
    Allow users to place bids
    Allow the creator to close the auction
    """

    listing = get_object_or_404(Listing, title=listing_title)

    # Watchlist Form
    watchlist_form = WatchListForm(request.POST or None)

    # Bid Form
    bid_form = BidForm(request.POST or None)

    # Close Auction Form
    close_auction_form = CloseAuctionForm(request.POST or None)

    # Comment Form
    comment_form = CommentForm(request.POST or None)

    # Handle Watchlist Form
    if request.method == 'POST' and watchlist_form.is_valid():
        action = watchlist_form.cleaned_data['action']
        user_watchlist = request.user.watchlist

        if action == 'add' and listing not in user_watchlist.listings.all():
            user_watchlist.listings.add(listing)
        elif action == 'remove' and listing in user_watchlist.listings.all():
            user_watchlist.listings.remove(listing)

        return HttpResponseRedirect(reverse("watchlist"))

    # Handle Bid Form
    if request.method == 'POST' and bid_form.is_valid():
        user_bid_amount = bid_form.cleaned_data['amount']

        # Check if the user's bid is greater than the current highest bid
        current_highest_bid = Bid.objects.filter(listing=listing).aggregate(Max('amount'))['amount__max']

        if current_highest_bid is not None and user_bid_amount > current_highest_bid:
            # Create a new bid record for the user
            new_bid = Bid(user=request.user, listing=listing, amount=user_bid_amount)
            new_bid.save()

            # Render the page with a success message
            return render(request, "auctions/listing_page.html", {
                "listing": listing,
                "watchlist_form": watchlist_form,
                "bid_form": bid_form,
                "bid_success_message": f"Successfully placed a bid of ${user_bid_amount}.",
                "close_auction_form" : close_auction_form,
                "comment_form": comment_form,
            })
        else:
            # Render the page with an error message that the bid was too low
            return render(request, "auctions/listing_page.html", {
                "listing": listing,
                "watchlist_form": watchlist_form,
                "bid_form": bid_form,
                "bid_error_message": "Bid amount is too low or there are no bids. Please enter a higher bid.",
                "close_auction_form" : close_auction_form,
                "comment_form": comment_form,
            })

    # Handle categories
    if request.method == 'POST':
        category_form = CategoryFilterForm(request.POST)
        if category_form.is_valid():
            selected_category = category_form.cleaned_data['category']
            if selected_category:
                filtered_listings = selected_category.listings.all()
                return render(request, 'auctions/categories.html', {
                    "listing": listing,
                    "watchlist_form": watchlist_form,
                    "bid_form": bid_form,
                    "close_auction_form" : close_auction_form,
                    "bid_success_message": f"Successfully placed a bid of ${user_bid_amount}.",
                    "comment_form": comment_form,
                })

    # Handle Close Auction Form
    if request.method == 'POST' and close_auction_form.is_valid():
        # Get the highest bid for the listing
        highest_bid = listing.bids

        if highest_bid:
            # Update Winner 
            listing.winner = highest_bid.user  # Set the winner to the user with the highest bid
            listing.is_active = False
            listing.save()

            return render(request, "auctions/listing_page.html", {
                "listing": listing,
                "watchlist_form": watchlist_form,
                "bid_form": bid_form,
                "bid_success_message": "Auction closed successfully!",
                "winner": f"{listing.winner} has won!",
                "close_auction_form" : close_auction_form,
                "comment_form": comment_form,
            })

    # Handle Comment Form
    if request.method == 'POST' and comment_form.is_valid():
        user_comment_text = comment_form.cleaned_data['text']

        # Create a new comment record for the user
        new_comment = Comments(user=request.user, listing=listing, text=user_comment_text)
        new_comment.save()

        # Redirect to the same page to avoid form resubmission
        return HttpResponseRedirect(reverse("listing_page", args=[listing_title]))
    
    # Check if user is creater
    user_is_creator = False
    if request.user == listing.created_by:
            user_is_creator = True

    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "watchlist_form": watchlist_form,
        "bid_form": bid_form,
        "close_auction_form": close_auction_form,
        "user_is_creator" : user_is_creator,
        "winner" : listing.winner,
        "comment_form": comment_form,
    })


@login_required
def watchlist(request):
    """
    Displays all listings added to the user's watchlist
    """
    # Get or create the user's watchlist
    user_watchlist = WatchList.objects.get_or_create(user=request.user)

    # Access the watchlist object from the tuple
    user_watchlist = user_watchlist[0]

    # Get listings from the user's watchlist
    listings = user_watchlist.listings.all()

    return render(request, 'auctions/watchlist.html', {
        'listings': listings
    })


def categories(request):
    """
    Allow user to filter listings by category
    Display listings based on category
    """
    selected_category = None

    if request.method == 'POST':
        category_form = CategoryFilterForm(request.POST)
        if category_form.is_valid():
            selected_category = category_form.cleaned_data['category']
            if selected_category:
                filtered_listings = selected_category.listings.all()
                return render(request, 'auctions/categories.html', {
                    'listings': filtered_listings, 
                    'selected_category': selected_category,
                    'category_form' : category_form
                })

    # For GET requests or invalid form submissions, display the form and all listings
    category_form = CategoryFilterForm()
    listings = Listing.objects.all()
    return render(request, 'auctions/categories.html', {
        'category_form': category_form, 
        'listings': listings, 
        'selected_category': selected_category}
        )


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

            # Create an empty watchlist for the new user
            watchlist = WatchList.objects.create(user=user)
            watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
