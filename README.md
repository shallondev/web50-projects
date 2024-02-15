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
    - Alternatively, articles can be rendered with /wiki/TITLE where TITLE is an exact match of the articles title, otherwise an error page will be rendered.
- Search Bar
    - The search bar located on the side bar allows users to search articles.
        - If the query is an exact match to the title of the article then the contents of the article will be rendered.
        - Otherwise, search results were the query was a substring of the title lower or upper case will be rendered for the user to select.
- Create New Page
    - Users can enter a title and content into a form that will be used to create a markdown file when submitted.
    - The content of the markdown file will then be converted to HTML to it can be rendered as an article.
- Random Page
    - Clicking on 'Random Page' will render a random artcle with its contents.
- Edit Entry
    - Selecting 'Edit Entry' while viewing a article will direct to the user to a form with the Title and Content allowed filled with that of the article they are viewing.
    - The user can change that title and contents of the article.
    - Submitting the changes will update the rendered HTML content of the article..