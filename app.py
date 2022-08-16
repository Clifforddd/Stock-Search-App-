"""Flask app for Stock app."""

from curses import flash
from flask_sqlalchemy import SQLAlchemy

import yfinance as yf
from flask import Flask, request, jsonify, render_template,redirect, session, flash
from models import db, connect_db, User, Profile
from forms import UserForm
from sqlalchemy.exc import IntegrityError
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stock_app'  #FIXME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret"                         

connect_db(app)


#Homepage   
@app.route("/")
def home_page():
    """Render homepage."""

    return render_template('base.html')

@app.route("/stock")
def stock():
    """Search Stock page"""
    try:
        if "symbol" not in request.args:
            return render_template('stock.html')
        else:    
            symbol = request.args["symbol"]
            ticker = yf.Ticker(symbol)

            price = {'Name':ticker.info['shortName'], 'Current Price':ticker.info['currentPrice']}
            # price.append(ticker.info['shortName'])
            # price.append(ticker.info['currentPrice'])

            #price = json.dumps(ticker.info)

            return render_template('stock.html', ticker=price)
    except:
        price = "No ticker found."
        return render_template('stock.html', ticker=price)



@app.route("/profile")
def profile_page():
    if "user_id" not in session:
        flash("Please login")
        return redirect('/')
    return render_template('profile.html')

@app.route('/profile/<int:id>', methods=["POST"])
def add_favo(id):
    """Add favorite stock to profile"""
    if 'user_id' not in session:
        flash("Please Login")
        return redirect('/login')

    ticker = Profile.query.get_or_404(id)
    if ticker.user_id == session['user_id']:

        symbol = request.args["symbol"]
        print(symbol)
        print(ticker.user_id)
        new_favo = Profile.register(symbol, ticker.user_id)

        db.session.add(new_favo)
        db.session.commit()
        flash("Added to Profile")
        return redirect("/profile")
    
    flash("No Permission to add")
    return redirect("/profile")

@app.route('/register', methods=['GET', 'POST'])
def register_user():
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
        return redirect('/register') # Might change route

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.username}.")
            session['user_id'] = user.id
            return redirect('/')
        else:
            form.username.errors = ['Invalid information.']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("You have successfully logged out")

    return redirect('/')