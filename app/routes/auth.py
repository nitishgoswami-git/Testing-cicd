from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash   # ✅ added for password hashing
from app.models import User
from app import db

auth_route = Blueprint('auth', __name__)

@auth_route.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # ❌ before: User.query.filter_by(name=username, password=password).first()
        #    wrong: mixing "name" vs "username", also filtering by password directly
        # ✅ fixed: check only username
        user = User.query.filter_by(username=username).first()

        if user:
            flash("User already exists", "danger")
        else:
            # ❌ before: storing plain password
            # ✅ fixed: hash password before saving
            new_user = User(
                username=username,
                password=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()

            session['user'] = username
            flash('Registration successful', 'success')

            # ❌ before: return redirect(url_for('/'))
            # ✅ fixed: must point to endpoint, not raw "/"
            return redirect(url_for('auth.home'))

    return render_template('register.html')


@auth_route.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        # ❌ before: User.query.filter_by(username=username).first() (fine)
        # ✅ kept same, but added password check
        user = User.query.filter_by(username=username).first()

        # ❌ before: only checked user, ignored password
        # ✅ fixed: verify hashed password with check_password_hash
        if user and check_password_hash(user.password, password):
            session['user'] = username
            flash('Login successful', 'success')
            return redirect(url_for('auth.home'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')


@auth_route.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out', 'info')

    # ❌ before: url_for('auth.login') was fine, kept same
    return redirect(url_for('auth.login'))


@auth_route.route('/')
def home():
    if 'user' not in session:
        # ❌ before: return redirect(url_for('login')) (wrong, no endpoint named 'login')
        # ✅ fixed: must use blueprint endpoint
        return redirect(url_for('auth.login'))

    # ❌ before: user = User.query.filter_by(username=user) → reused variable incorrectly
    # ✅ fixed: fetch username from session and query properly
    username = session.get('user')
    user = User.query.filter_by(username=username).first()

    return render_template('home.html', user=user)
