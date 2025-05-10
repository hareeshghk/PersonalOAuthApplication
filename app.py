# app.py
import os
import json
from flask import Flask, redirect, url_for, session, render_template, jsonify
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') # Needed for session management

if (app.secret_key == None):
    raise "Secret key missing."

# Configure OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # OIDC Userinfo endpoint
    client_kwargs={'scope': 'openid email profile'},
    # For older versions of Authlib, you might need server_metadata_url:
    # server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

@app.route('/')
def index():
    """
    Home page.
    Shows login/register button if not logged in.
    Shows profile link and logout if logged in.
    """
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login/google')
def login_google():
    """
    Redirects to Google's OAuth 2.0 server to initiate authentication.
    """
    # The redirect_uri must match exactly what you configured in Google Cloud Console
    redirect_uri = url_for('auth_google', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/callback/google')
def auth_google():
    """
    Callback route that Google redirects to after user authentication.
    Fetches the access token and user information.
    """
    try:
        token = google.authorize_access_token()
        # The userinfo endpoint is automatically called by .userinfo() if configured
        # or by fetching the token if 'openid' scope is used and userinfo is in id_token.
        # resp = google.get('userinfo') # This works too if userinfo_endpoint is set
        # user_info = resp.json()
        # Authlib 0.15+ provides userinfo in the token directly if 'openid' scope is used.
        user_info = token.get('userinfo')
        if not user_info: # Fallback if not in token directly
            user_info = google.userinfo(token=token)


    except Exception as e:
        app.logger.error(f"Error during Google OAuth callback: {e}")
        return f"Authentication failed: {e}", 400

    # Store user information in the session
    # You might want to fetch/create a user in your database here
    session['user'] = user_info
    session['google_token'] = token # Storing the whole token for inspection if needed

    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    """
    Displays user profile information fetched from Google.
    """
    user = session.get('user')
    if not user:
        return redirect(url_for('index'))
    
    # For display purposes, let's pretty print the user info
    user_info_pretty = json.dumps(user, indent=4)
    return render_template('profile.html', user=user, user_info_pretty=user_info_pretty)

@app.route('/logout')
def logout():
    """
    Logs the user out by clearing the session.
    """
    session.pop('user', None)
    session.pop('google_token', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Ensure FLASK_DEBUG is set in .env or here
    app.run(debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true', port=5000)