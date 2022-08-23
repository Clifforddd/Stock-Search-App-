"""Flask app for Stock app."""
from curses import flash
from flask_sqlalchemy import SQLAlchemy

import yfinance as yf
from flask import Flask, request, jsonify, render_template,redirect, session, flash
from models import db, connect_db, User, Profile
from forms import UserForm, FavoForm
from sqlalchemy.exc import IntegrityError
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stock_app'  #FIXME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret"                         

connect_db(app)

app.run(debug=True)
#Homepage   
@app.route("/")
def home_page():
    """Render homepage."""

    return render_template('homepage.html')

@app.route("/stock")
def stock():
    """Search Stock page"""
    
    try:
        if "symbol" not in request.args:
            return render_template('stock.html')
        else:    
            symbol = request.args["symbol"]
            id = request.args["id"]
            ticker = yf.Ticker(symbol).info
    
            price = {'Name':ticker['shortName'], 'Symbol': ticker['symbol'], 
            'Current Price':ticker['currentPrice'], 'Earnings Growth': ticker['earningsGrowth'],
            'Current Ratio':ticker['currentRatio'], 'Profit Margins': ticker['profitMargins']   
            }
            q = Profile.query.filter(Profile.favo == symbol).filter(Profile.user_id == id).all()
            
            return render_template('stock.html', ticker=price, q=q)
    except:
        price = {'Error': 'No ticker found'}
        return render_template('stock.html', ticker=price)



@app.route("/add_favo", methods=["GET"])
def profile_page():
    """Add favorite stock into Profile"""
    if "user_id" not in session:
        flash("Please login")
        return redirect('/')
    
    user_id = session['user_id']
    user_favo = Profile.query.filter_by(user_id = f"{session['user_id']}").all()
    
    #----
    favos = []
    for i in user_favo:
        favos.append(i.favo)
    tickers = yf.Tickers(' '.join(favos)).tickers
    #----
    
    arr = []

    for t in tickers:
        # symbol = u.favo
    
        # ticker = yf.Ticker(symbol)

        price = {'Name':tickers[t].info['shortName'], 'Symbol': tickers[t].info['symbol'], 
        'Current Price':tickers[t].info['currentPrice'], 'Earnings Growth': tickers[t].info['earningsGrowth'],
        'Current Ratio':tickers[t].info['currentRatio'], 'Profit Margins': tickers[t].info['profitMargins']   
        }

        arr.append(price)
    
    return render_template('profile.html', tickers=arr, user_id=user_id)

@app.route('/add_favo', methods=["POST"])
def add_favo():
    """Validate favorite stock is in database or not, if in database, remove favorite."""
    favo_stock = request.form["favo"]
    user_id = request.form["user_id"]

    q = Profile.query.filter(Profile.favo == favo_stock).filter(Profile.user_id == user_id).all()


    if len(q) == 1:
        db.session.delete(q[0])
        db.session.commit()
    
        flash("Removed favorite stock!")

        return redirect(request.referrer)


    else:
        new_fav = Profile(favo_stock, user_id)

        db.session.add(new_fav)
            
        db.session.commit()

        flash("Added to your profile!")

        return render_template('profile.html', favo=favo_stock, user_id=user_id)


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Register a user"""
    form = UserForm()

    if form.validate_on_submit():

        username = form.username.data
 
        password = form.password.data

        new_user = User.register(username, password)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id
        flash('Account Created')
        return redirect('/') # Might change route

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Login a user"""

    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.username}.")
            session['user_id'] = user.id
            session['user_name'] = user.username
            return redirect('/')
        else:
            form.username.errors = ['Invalid information.']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("You have successfully logged out")

    return redirect('/')