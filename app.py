"""
This Flask application provides a simple login system with signup and settings pages.

The application has four routes:
- Login ('/'): Renders a login page where users can enter their username 
and password to authenticate. If successful,
the user is redirected to their home page ('/home'). If unsuccessful, 
an error message is displayed.
- Logout ('/logout'): Logs the user out by clearing their session data and redirecting them to 
the login page.
- Signup ('/signup'): Renders a signup page where users can enter a 
new username, password, and email address to create
a new account. If successful, the user is automatically logged in and redirected to
 their home page. If unsuccessful,
an error message is displayed.
- Settings ('/settings'): Renders a settings page where users can change their password and/or email 
address. If
changes are made, the user's information is updated in the database.

The application uses several helper functions in the 'helpers.py' module to manage user 
authentication and database interactions.
"""


import json
import os
from flask import Flask, redirect, url_for, render_template, request, session
from scripts import forms
from scripts import helpers


app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only

# Heroku
#from flask_heroku import Heroku
#heroku = Heroku(app)

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def login():
    """
    This function handles the login page, which is the root page of the website.

    GET requests return a page containing a form for entering login credentials.
    POST requests handle form submissions and either log the user in or display an error message.

    Returns:
        If the user is not logged in, the function returns a login page.
        If the user is logged in, the function returns the home page.
    """
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = request.form['password']
            if form.validate():
                if helpers.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    user = helpers.get_user()
    return render_template('home.html', user=user)

@app.route("/logout")
def logout():
    """
    This function handles the logout functionality.

    When a user logs out, their session is ended and they are redirected to the login page.

    Returns:
        A redirect to the login page.
    """
    session['logged_in'] = False
    return redirect(url_for('login'))


# -------- Signup ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    This function handles the signup page.

    GET requests return a page containing a form for creating a new account.
    POST requests handle form submissions and either create the account or display an error message.

    Returns:
        If the user is not logged in, the function returns a signup page.
        If the user is logged in, the function redirects to the home page.
    """
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = helpers.hash_password(request.form['password'])
            email = request.form['email']
            if form.validate():
                if not helpers.username_taken(username):
                    helpers.add_user(username, password, email)
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Signup successful'})
                return json.dumps({'status': 'Username taken'})
            return json.dumps({'status': 'User/Pass required'})
        return render_template('login.html', form=form)
    return redirect(url_for('login'))


# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """
    This function handles the settings page, where users can change their account information.

    GET requests return a page containing a form for changing the user's password and email address.
    POST requests handle form submissions and update the user's account information.

    Returns:
        If the user is logged in, the function returns the settings page.
        If the user is not logged in, the function redirects to the login
    """
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))


@app.errorhandler(404)
def invalid_route(e):
    """
    This function handles 404 errors.
    """
    return jsonify({'errorCode' : 404, 'message' : 'Route not found'})

# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0")
