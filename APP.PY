from flask import Flask, redirect, url_for, request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import firebase_admin
from firebase_admin import credentials, storage
import json
from cryptography.fernet import Fernet

import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)

with open('filekey.key', 'rb') as filekey:
    key = filekey.read()
fernet = Fernet(key)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('firebase_secrets.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'enter-bucket-name-here'
})

@app.route('/')
def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        ['https://www.googleapis.com/auth/calendar']
    )
    flow.redirect_uri = url_for('callback', _external=True)
    authorization_url, _ = flow.authorization_url(prompt='consent')
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        ['https://www.googleapis.com/auth/calendar']
    )
    flow.redirect_uri = url_for('callback', _external=True)
    flow.fetch_token(authorization_response=request.url)

    # Get the user's email
    service = build('calendar', 'v3', credentials=flow.credentials)
    profile = service.calendarList().get(calendarId='primary').execute()
    email = profile['id']

    # Serialize and save credentials to Firebase Storage
    serialized_credentials = json.dumps({
        'token': flow.credentials.token,
        'refresh_token': flow.credentials.refresh_token,
        'token_uri': flow.credentials.token_uri,
        'client_id': flow.credentials.client_id,
        'client_secret': flow.credentials.client_secret,
        'scopes': flow.credentials.scopes
    })

    bucket = storage.bucket()
    blob = bucket.blob(email)
    # encrypted_serialized_credentials = fernet.encrypt(serialized_credentials)
    blob.upload_from_string(serialized_credentials)

    return '''
    <html>
        <head>
            <meta http-equiv="refresh" content="2;url=http://localhost:3000">
        </head>
        <body>
            <p>Authentication Complete, Redirecting.........</p>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
