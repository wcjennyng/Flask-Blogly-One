"""Blogly application."""

from flask import Flask, request, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    """Homepage"""
    return redirect('/users')

@app.route('/users')    
def users_index():
    """List of users page"""

    users = User.query.all()
    return render_template('/users/index.html', users=users)

@app.route('/users/new_user', methods=['GET'])
def new_user_page():
    """Shows a form for new user (get request)"""
    return render_template('/users/new_user.html')

@app.route('/users/new_user', methods=['POST'])
def new_user_form():
    """Handle form submission for creating a new user (post request)"""

    new = User(first_name=request.form['first_name'], last_name=request.form['last_name'], image_url=request.form['image_url'] or None)

    db.session.add(new)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_page(user_id):
    """Show information about given user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/user_page.html', user=user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show the edit page for a user (get request)"""

    user = User.query.get_or_404(user_id)
    return render_template('/users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def users_update(user_id):
    """Process the edit form to update an existing user (post request) """
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def users_delete(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')