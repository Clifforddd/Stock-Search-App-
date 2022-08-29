# Stock-Search-App

### API name: yfinance
### API Link: https://pypi.org/project/yfinance/

## Function:
  Users could search stocks in this app, and register account save their favorite stocks in their profile.
  
  In "Search Stock" section, users could type stock ticker for search. After click search, they would see a star button in front of the ticker to save it as favorite stock.
  In "Profile" section, users could find their saved stocks.
  Users have to register an account and log in to save stocks. As tourist, they do not have the permission to save stocks. All passwords have been hashed safely in database.
  
## App Set up: 
Please **download** required libararies from **requirments.txt**. You could type this in Terminal: pip install -r requirements.txt

Create database using PostgreSQL. Run seed.py to create database: Python seed.py

To run the local termial type this in Terminal: flask run

**Copy localhost URL** to Chrome or Safari or other Browser to test the app.

## Heroku app link:
https://cliff-stock-search-app.herokuapp.com/

## Tool used in this App:
Main language uses in this app is **Python** as back-end tool. Also, include **FLASK**, SQLAlchemy, Jinja, Wtforms, RESTFUL API structure, HTML, CSS, Heroku.
