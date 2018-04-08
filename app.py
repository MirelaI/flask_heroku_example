import os
from flask import Flask

app = Flask('MyHerokuApp')

mailgun_secret_key = os.environ.get('MAILGUN_SECRET_KEY', None)

@app.route('/')
def index():
    # We will just display our mailgun secret key, nothing more.
    return render_template("index.html", mailgun_secret_key)

app.run(debug=True)