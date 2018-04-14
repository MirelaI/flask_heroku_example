import os
from flask import Flask, render_template

app = Flask('MyHerokuApp')

# Read the mailgun secret key from environment variables
mailgun_secret_key_value = os.environ.get('MAILGUN_SECRET_KEY', None)

# This is needed for Heroku configuration, as in Heroku our
# app will probably not run on port 5000, as Heroku will automatically
# assign a port for our application
port = int(os.environ.get("PORT", 5000))

@app.route('/')
def index():

    # We will just display our mailgun secret key, nothing more.
    return render_template("index.html", value=mailgun_secret_key_value)

# Route that will get the config value based on a provided key, so in
# this way we can interogate our configuration.
@app.route('/<config_key>')
def key(config_key=None):
    config_value=None

    if (config_key):
        # Advice: You should make a convention to define config key upper cased.
        # otherwise you will have consistency issues when reading your keys.
        # If you know they are always upper cased, you just need to uppercase
        # what the config_key argument.
        config_key = config_key.upper()
        config_value = os.environ.get(config_key, None)

    if key and config_value:
        app.logger.info("Value of {} is {}.".format(config_key, config_value))

    # We will just display our mailgun secret key, nothing more.
    return render_template("keys.html", key=config_key, value=config_value)

app.run(host='0.0.0.0', port=port, debug=True)
