import os
from flask import Flask, render_template

app = Flask('MyHerokuApp')

mailgun_secret_key = os.environ.get('MAILGUN_SECRET_KEY', None)

@app.route('/')
def index():
    # We will just display our mailgun secret key, nothing more.
    return render_template("index.html", key=mailgun_secret_key)

app.run(debug=False, host='0.0.0.0', port=environ.get("PORT", 5000))