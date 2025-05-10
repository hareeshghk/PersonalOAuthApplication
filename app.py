# Author: Hareesh Kumar Gajulapalli
import json
from config import config
from flask import Flask, redirect, url_for, session, render_template, jsonify
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Configure OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    client_kwargs={'scope': 'openid email profile'},
    # contains metadata or various endpoints needed.
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    claims_options={
        'iss': {
            'essential': True,
            'values': ['https://accounts.google.com', 'accounts.google.com']
        }
    }
)

@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login/google')
def login_google():
    # The redirect_uri must match with what we configured in Google Cloud Console for Oauth application.
    redirect_uri = url_for('auth_google', _external=True)
    app.logger.info(f"Redirecting to Google with redirect_uri: {redirect_uri}")
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/callback/google')
def auth_google():
    try:
        app.logger.debug("Attempting to authorize access token from Google...")
        token = google.authorize_access_token()
        app.logger.info("Successfully authorized access token.")
        app.logger.debug(f"Token received: {token}")

        user_info = token.get('userinfo')
        # Fallback if not in token directly
        if not user_info:
            app.logger.warning("Userinfo not found in token, attempting to fetch from userinfo_endpoint.")
            user_info = google.userinfo(token=token)
        app.logger.info(f"User info processed: {user_info}")

        # Storing user information in the session
        # <for application use this place for storing user information in your database>
        session['user'] = user_info
        session['google_token'] = dict(token)

        return redirect(url_for('profile'))


    except Exception as e:
        app.logger.error(f"Error during Google OAuth callback: {type(e).__name__} - {e}")
        # Print the full traceback for more details during debugging
        import traceback
        app.logger.error(traceback.format_exc())
        return f"Authentication failed: {type(e).__name__} - {e}", 400

    

@app.route('/profile')
def profile():
    user = session.get('user')

    if not user:
        return redirect(url_for('index'))
    
    # For display purposes, let's pretty print the user info
    user_info_pretty = json.dumps(user, indent=4)
    
    return render_template('profile.html', user=user, user_info_pretty=user_info_pretty)

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('google_token', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # FLASK_DEBUG is default flase, set in .env if needed.
    app.run(debug=config.FLASK_DEBUG, port=5000)