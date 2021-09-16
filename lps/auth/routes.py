from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_user, logout_user, current_user
from lps import db
from lps.models import User
from lps.forms import *


auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth", template_folder="templates")


# Login Page
@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password_hash(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid Username')
            return redirect(url_for('auth_bp.login'))

    return render_template('login.html', form=form)


# Signup Page
@auth_bp.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            new_user = User(form.username.data, form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('index'))
        flash('A user already exists with that email address.')
    
    return render_template('signup.html', form=form)


# Logout Endpoint
@auth_bp.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()

    return redirect(url_for('auth_bp.login'))
