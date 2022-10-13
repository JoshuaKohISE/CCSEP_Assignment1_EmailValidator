from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
#Import Regular Expression 
import re

# This time, instead of using regex, we will be using the library email_validator to perform
# the email validation
from email_validator import validate_email, EmailNotValidError

auth = Blueprint('auth', __name__)
#The Evil Regex
#emailRegex= re.compile(r'^([a-zA-Z0-9])(([\-.]|[_]+)?([a-zA-Z0-9]+))*(@){1}[a-z0-9]+[.]{1}(([a-z]{2,3})|([a-z]{2,3}[.]{1}[a-z]{2,3}))$')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #Call the check() function to validate email
        if check(email) is True:
            flash('Valid Email!')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Function to check whether or not the password contains user's first name
def check_password(username, password):
    checkPassRegex = re.compile(username)
    if re.search(checkPassRegex, password) is not None:
        return True
    else:
        return False

#Function to check the validity of email using validate_email from email_validator library
def check(email):
    try:
        #Call the validate_email function to validate the email inputted
        em = validate_email(email)
        #If the email is valid,
        #Replace the email with its normalised form
        emailPassed = em.email
        return True;
    except EmailNotValidError as e:
        #Show a prompt for the error in human-readable form
        flash(str(e), category = 'error')
        return False;
        
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        # Check to see if it is a valid email
        # Call the check() function to validate email
        elif check(email) is False:
        	flash('Invalid Email Address! Please try again.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        # Checks to see if the password contains the user's First Name
        elif check_password(request.form.get('firstName'), password1) is True:
            flash('Password must not include your first name!', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
