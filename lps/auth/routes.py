from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import login_user, logout_user, current_user
from lps import db, login_manager
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
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid Username', 'danger')
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
        flash('A user already exists with that email address.', 'danger')
    
    return render_template('signup.html', form=form)


# Logout Endpoint
@auth_bp.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('auth_bp.login'))


# LOGIN MANAGER ROUTES
@login_manager.user_loader
def load_user(email):
    if email is not None:
        return User.query.filter_by(email=email).first()
    return None


@login_manager.unauthorized_handler
def unauthorized():
    # Redirect unauthorized users to Login page.
    flash('You must be logged in to view that page.', 'danger')
    return redirect(url_for('auth_bp.login'))