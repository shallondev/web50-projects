# Collection of CS50's Introduction to Web Programming Projects

## Table of Contents

## Search
A front-end design of google search.

### Introduction
Using HTML forms you can GET the parameters of a google search query. This project utilizes this fact to build a front-end design similar in nature to google.com using HTML and CSS.

### Usage
Download and open search-shallondev on your local machine and open index.html in a browser.

### Specification
- index.html replicates google's homepage by incorporating Google Search and I'm Feeling Lucky.
- image.html replicates google's image search.
- advanced.html replicates google's advanced search functionality.

### Awknowldgements
This project used distribution code provided by CS50 https://cs50.harvard.edu/web/2020/projects/0/search/

## Wiki
A online encylcopedia with markdown and django.

### Introduction
An encyclopedia is a reference compendium containing articles that can cover various subjects and fields of knowledge. Markdown is a markup language used to write formatted text in a simple and easy-to-read manner such as this document.

This project aims to create an online encyclopedia using Django. Users will be able to search, read, create, and edit article entries written in Markdown.

### Usage
```bash
cd wiki-shallondev
python3 manage.py runserver
``` 

### Requirments
python3, django, python-markdown2

```bash
pip3 install django
pip3 install markdown2
```

### Specification
- Home
    - Clicking 'Home' will display all article entries that can be rendered by clicking on their title.
    - Alternatively, articles can be rendered with the URL /wiki/TITLE where TITLE is an exact match of the articles title, otherwise an error page will be rendered.
- Search Bar
    - The search bar located on the side bar allows users to search for articles.
        - If the query is an exact match to a title of an article then the contents of the article will be rendered.
        - Otherwise, search results will be rendered where the query was a substring of a article's title.
- Create New Page
    - Users can enter the title and content into a form that will be used to create a markdown file when submitted.
    - The content of the markdown file will then be converted to HTML so that it can be rendered as an article.
- Random Page
    - Clicking on 'Random Page' will render a random artcle with its contents.
- Edit Entry
    - Selecting 'Edit Entry' while viewing a article will direct the user to a form with the title and content of that article.
    - The user can change that title and contents of the article.
    - Submitting the changes will update the rendered HTML content of the article.
- Styling
    - a CSS stylesheet is used to make the application look more beautiful.

### Awknowldgements
This project used distribution code provided by CS50 https://cs50.harvard.edu/web/2020/projects/1/wiki/

## Commerce
A full-stack e-commerce auction site built with django and sqlite3.

### Introduction
A e-commerce site similar in nature to sites like Ebay allow users to post listings of items that other users can place bids on. Once an auction has closed the user who has placed the highest bid will win the listed item at the price of their bid. 

This project creates a web application where authenticated users can create listings of items they wish to sell, make bids on other users active listings, search for items by category, and create a 'watchlist' of listings. A watchlist is similar to a wishlist in which user can add active listings they want to watch.

### Usage
```bash
cd commerce-shallondev
python3 manage.py runserver
```

### Requirments
python3, django

```bash
pip3 install django
```

### Specification
- The following SQL models are used: Listing, Categorie, Watchlist, Bid, Comment.
    - All models are registered with django-admin and can be manipulated within the web application.
- Active Listing
    - Displays all listings that are active in that bids can be made and no winner has been decided.
    - Displays basic information the user should know about the listing and a button to view the listing itself.
- View
    - Displays information such as the current price, who owns the listing, a description of the listing.
    - Authenticated users can place a bid on the listing.
    - Authenticated users can add or remove the listing to their watch list.
    - Authenticated user can make and view comments on the listing.
    - The listing owner can close the auction.
    - Closed auctions display a winner.
- Categories
    - Renders a form that allows users to select a category to submit.
    - Upon submission displays all listings inside the cateogory the user selected.
    - Listings are stored by title in the cateogories model.
- Watchlist
    - Displays all listings that are on the signed in users watchlist
    - Not accessible if user is not singed in.
    - Watchlist items are held in the watchlist model specifc to the current user.
- Create New Listing
    - Creates a form that allows users to input a title, description, price, image url, and category of a listing the user once to post.
    - The process of creating the listing is handled by our Listing model.
- User authentication
    - Uses django User model to create authenticated users.
    - Users can register, sign in, and sign out.
- Styling
    - CSS and boostrap are used to make the web application look beautiful.

### Awknowldgements
This project used distribution code provided by CS50 https://cs50.harvard.edu/web/2020/projects/2/commerce