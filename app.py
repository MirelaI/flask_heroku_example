import os
from flask import Flask, render_template

app = Flask('MyHerokuApp')

# Read the mailgun secret key from config variables
mailgun_secret_key = os.environ.get('MAILGUN_SECRET_KEY', None)

# This is needed for Heroku configuration as in Heroku our
# app will porbably not run on port 5000 as Heroku will automatically
# assign a port for our application
port = int(os.environ.get("PORT", 5000))

@app.route('/')
def index():
    # We will just display our mailgun secret key, nothing more.
    return render_template("index.html", key=mailgun_secret_key)

app.run(host='0.0.0.0', port=port, degubs=True)