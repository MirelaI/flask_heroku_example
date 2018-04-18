# Heroku Flask application

This example sets a simple Flask app in Heroku while also reading configuration variables. Configuration variables are a great way for us to store secret keys without publishing them to GitHub.

We saw in [Flask Config example](https://github.com/MirelaI/flask_config_example) how we can setup our configuration in a JSON formatted file and in the same time keep the configuration hidden in our GitHub repository while using [.gitignore](https://help.github.com/articles/ignoring-files/). These were the basic steps to achieve our goal: NOT to publish our secret keys to GitHub.

Now, you might wonder, but how this will work in Heroku? As I still need to push the code on the Heroku remote master branch to deploy my application and if I keep my secret keys away from Github, Heroku will not know from where to read them. Will demo step by step how this is possible, so please join me in this journey.

This example shows you how you can setup your application to be deployable in Heroku and also still keep your keys secret. Do not worry if the steps for keeping your keys secret are not the same as in the [Flask Config example](https://github.com/MirelaI/flask_config_example) example, because this example had to be adapted to work best with Heroku, but the principle is the same. We are just going to use a different type of configuration file.

_Note: this example starts from zero and some files might be different from what you have in the current setup. If you already have your project setup and working, you do __NOT__ need to follow the steps in [`Create a Flask application`](https://github.com/MirelaI/flask_heroku_example#create-a-flask-application). You can skip until [`Setup Heroku`](https://github.com/MirelaI/flask_heroku_example#setup-heroku) section and be aware your application files are different than mine so you your file names and that some output that I've provided might be a bit different from yours. For example my flask application sits in `app.py`, yours might be named totally different, so use your filename when you see in my example `app.py`._

_Note 2: You will see me mentioning in this demo either config variables or environment variables, I am referring to the same thing :) as we are going to use environment variables in order to store any configuration that we need for our application._

Here we go...

## Create a Flask application

### Create your git repository

You need to login into your GitHub repository and create your project repository. Once you've done that, go to your terminal and make a local copy of your repository and cd into it. See below the terminal commands:

```bash
git clone <your_repo_url>
cd your_repo_folder
```

### Make a simple Flask app using Jinjia
I've created the following files.

```bash
touch app.py README.md
mkdir templates
touch templates/index.html
```

At this point you should have the following structure:

```bash
.
├── README.md
├── app.py
└── templates
    └── index.html
```

In the `app.py` file, define a simple Flask app using the flask python module. See code below:

```python
import os
from flask import Flask, render_template

app = Flask('MyHerokuApp')

# We will set this up a bit later, do not worry if we leave it as None for now.
mailgun_secret_key_value = None

@app.route('/')
def index():

    # We will just display our mailgun secret key, nothing more.
    return render_template("index.html", value=mailgun_secret_key_value)

app.run(debug=True)
```

I've saved the file and now, since the `index()` method renders the `index.html` template, I need to define the template. Edit `templates/index.html` to contain the code below:

```html
<!doctype html>
<html>
    <head>
        <title>My Checking Config Values APP</title>
    </head>

    <body>
        {% if value %}
        <p>Value: {{value}}!</p>
        {% else %}
        <p>No value defined!</p>
        {% endif %}
    </body>
</html>
```

Now let's run the app locally. In your terminal, at the root of your `your_repo_folder` that cd into at the first step, start the application:

```bash
python app.py
```

This will start your server at _http://localhost:5000/_. When you access in your web browser this page your should see _No value defined!_. This is because our Flask application has no idea from where to read your mailgun secret key. Let's come to this a bit later and focus now on setting up our heroku app.

## Setup Heroku

In this section we are going to focus on how setup our application to be Heroku compatible. In order to make our application to run on Heroku we need to add the following files:

### Procfile

This file is required as it is the file where you define what command Heroku should run in order to start your application. Be sure you create this file in your root directory, ie: `your_repo_folder` that you cd-ed in your first step.

```bash
touch Procfile
```

Add the following line in your `Procfile`:
```
web: python app.py $PORT
```

For now the line above is enough, as we are saying to Heroku start my `web` server with the `python app.py` on the port `$PORT`. **The command `python app.py` that I set in the Procfile is the exact command that I use to start my Flask application from my terminal. If your command is different, amend the Procfile to be sure it has the right start up command.***

Port is the 5000 that you see when you start the application from your terminal. _http://localhost:5000/_. But since Heroku assignes random port numbers for each application we need to let Heroku read the port that it defined for our application. Hence trailing `$PORT` when we define our startup command.

If you want different setups when you start your app, please have a read through [Prodfile documentation](https://devcenter.heroku.com/articles/procfile).

### Dependencies

Each application has some dependencies. For example we use Flask, that is a dependency that we needed to install on our local machine with pip when we started using Flask. Now Heroku does not know at this point that we need Flask. We can let Heroku know that we need Flask by defining a new file at the root of `your_repo_folder` that will contain our dependencies, like Flask and Jinja.

Create a new file named `requirements.txt`:

```bash
touch requirements.txt
```
And edit it to contain the following lines:

```
flask==0.12.2
Jinja2==2.6
```

### What python version should Heroku run?
You need to specify what python version are you using to run your application so Heroku will install the same version. You achieve this by creating a new file named `runtime.txt`

```bash
touch runtime.txt
```

Add the following line in the `runtime.txt`:
```
python-2.7.14
```
Note: you might use different python versions, please add in the `runtime.txt` the version that suites you most.

### One more thing

There is one small change that we need to do in order for our application to run on Heroku environment. Remember the $PORT trailing when we setup our startup run command. We need now to make sure our application will pickup the port that heroku will setup for us. In order to do that we need to edit `app.py` file and make some adjustments.

In short, we need to import a library that will let us read the environment variables that Heroku will set at initialization, like the application port. That library is called `os`.

```python
import os
```

Using this library we read the port and in the same time we make sure that the port will be an integer by appling the method `int` to the port.

```python
port = int(os.environ.get("PORT", 5000))
```
If no port is defined, 5000 will be used as a default port, ie: when we run our application locally the port will be 5000 as we have no environment port variable defined. Last we need to make sure that the application will start on the specific port:

```python
app.run(host='0.0.0.0', port=port, debug=True)
```

This is how your code should look after the adjustments above. You can see the adjustments we made to the initial code as they are marked with a `ADJUSTMENT` comment.

```python
from flask import Flask, render_template

# ADJUSTMENT: import the library that will let us read environment variables
import os

app = Flask('MyHerokuApp')

# We will set this up a bit later, do not worry if we leave it as None for now.
mailgun_secret_key_value = None

# ADJUSTMENT: This is needed for Heroku configuration as in Heroku our
# app will porbably not run on port 5000 as Heroku will automatically
# assign a port for our application.
port = int(os.environ.get("PORT", 5000))

@app.route('/')
def index():

    # We will just display our mailgun secret key, nothing more.
    return render_template("index.html", value=mailgun_secret_key_value)

# ADJUSTMENT: Setup our application to run with the needed port.
app.run(host='0.0.0.0', port=port, debug=True)
```

### Let's deploy

At this point your folder structure should look something simillar to the one below:

```
.
├── Procfile
├── README.md
├── app.py
├── requirements.txt
├── runtime.txt
└── templates
    └── index.html
```

You should also have Heroku CLI setup, if not please follow the steps [here](https://devcenter.heroku.com/articles/heroku-cli).

Type the following command:

```bash
heroku create
```
Here is the output that I saw in my console, bear in mind, you for sure will have different URLs:

```bash
heroku create
Creating app... done, ⬢ murmuring-oasis-31169
https://murmuring-oasis-31169.herokuapp.com/ | https://git.heroku.com/murmuring-oasis-31169.git
```

Heroku will create an URL for your application and also a git repository from where Heroku will read your application code. So what is missing? Well Heroku created a repository but it's empty! We need to push our code to the new Heroku remote repository.

_Note: in order to see what remote repositories you have setup for the current folder run `git remote -v` command. You should see the origin and heroku remote repositories._

Let's commit our changes and push them to Heroku.

```bash
git status
```

I have the following output, yours might be different:
```bash
git status
On branch master

Initial commit

Untracked files:
  (use "git add <file>..." to include in what will be committed)

    Procfile
    README.md
    app.py
    requirements.txt
    runtime.txt
    templates/

nothing added to commit but untracked files present (use "git add" to track)
```

I am happy with my changes, will go ahead and commit them:
```bash
git add .
git commit -am 'My first Flask app in Heroku'
```

Now that I have my changes commited, I need to make Heroku aware of them, so let's go ahead and push them to the Heroku repository.

```
git push heroku master
```

My output is a bit noisy as it will install all the dependencies, this only happens the first time when you push.
```bash
git push heroku master
Counting objects: 9, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (4/4), done.
Writing objects: 100% (9/9), 1.09 KiB | 0 bytes/s, done.
Total 9 (delta 0), reused 0 (delta 0)
remote: Compressing source files... done.
remote: Building source:
remote:
remote: -----> Python app detected
remote: -----> Installing python-2.7.14
remote: -----> Installing pip
remote: -----> Installing requirements with pip
remote:        Collecting flask==0.12.2 (from -r /tmp/build_c05b15613af1246cf64e01279a966683/requirements.txt (line 1))
remote:          Downloading Flask-0.12.2-py2.py3-none-any.whl (83kB)
remote:        Collecting Jinja2==2.6 (from -r /tmp/build_c05b15613af1246cf64e01279a966683/requirements.txt (line 2))
remote:          Downloading Jinja2-2.6.tar.gz (389kB)
remote:        Collecting itsdangerous>=0.21 (from flask==0.12.2->-r /tmp/build_c05b15613af1246cf64e01279a966683/requirements.txt (line 1))
remote:          Downloading itsdangerous-0.24.tar.gz (46kB)
remote:        Collecting click>=2.0 (from flask==0.12.2->-r /tmp/build_c05b15613af1246cf64e01279a966683/requirements.txt (line 1))
remote:          Downloading click-6.7-py2.py3-none-any.whl (71kB)
remote:        Collecting Werkzeug>=0.7 (from flask==0.12.2->-r /tmp/build_c05b15613af1246cf64e01279a966683/requirements.txt (line 1))
remote:          Downloading Werkzeug-0.14.1-py2.py3-none-any.whl (322kB)
remote:        Installing collected packages: itsdangerous, click, Werkzeug, Jinja2, flask
remote:          Running setup.py install for itsdangerous: started
remote:            Running setup.py install for itsdangerous: finished with status 'done'
remote:          Running setup.py install for Jinja2: started
remote:            Running setup.py install for Jinja2: finished with status 'done'
remote:        Successfully installed Jinja2-2.6 Werkzeug-0.14.1 click-6.7 flask-0.12.2 itsdangerous-0.24
remote:
remote: -----> Discovering process types
remote:        Procfile declares types -> web
remote:
remote: -----> Compressing...
remote:        Done: 30.3M
remote: -----> Launching...
remote:        Released v3
remote:        https://murmuring-oasis-31169.herokuapp.com/ deployed to Heroku
remote:
remote: Verifying deploy... done.
To https://git.heroku.com/murmuring-oasis-31169.git
 * [new branch]      master -> master
```

You should have your application available to access at the URL that Heroku created for you, in my case https://murmuring-oasis-31169.herokuapp.com/. When accessing in your browser the URL you should see the same output as when we run the app locally:

```
No value defined!
```

SUCCESS, we deployed our first app in Heroku. So everytime we do some changes to our code we need to make sure we deploy, ie. push our code to heroku remote repository.

If anything goes wrong and your application is not running, you can see the application logs with the command below:

```bash
heroku logs
```

We are not fully done though. We need to make sure our origin repository is also at the latest version:
```bash
git push origin master
```
Now we have our application deployed and our Github repository is up to date with our code so our colleagues can pull to get the latest changes.

## Setup our secret keys
When we've setup the port above, we noticed that Heroku works nicely in reading environment variables and those for sure are not setup in git. They are setup on the webserver where your application runs. This is awesome, because it means we will be able to setup our secret keys in some environment variables!


### Setup local environment variables
First let's learn how we set those variables locally and make use of them in our code.

I can see in the [Heroku documentation](https://devcenter.heroku.com/articles/heroku-local#set-up-your-local-environment-variables), that I can start my application locally using heroku command line. Let's try to run the command and see what happens:

```bash
heroku local
```

Here is my output:
```bash
[WARN] No ENV file found
13:01:49 web.1   |   * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
13:01:49 web.1   |   * Restarting with stat
13:01:50 web.1   |   * Debugger is active!
13:01:50 web.1   |   * Debugger PIN: 782-892-076
```
Perfect, Heroku started my app on my local environmnet, and now I am able to access it via: http://0.0.0.0:5000/ or http://localhost:5000/. You can see that it gives you a warn that there is not ENV file in our project. It's really important to remember that in the ENV file, named `.env` is where the environemnt variables will be defined. These `.env` variables will only be available locally.

Create the `.env` file in the root of your repository folder, `your_repo_folder`:
```
touch .env
```
And let's define some environemnt variables in it. Add the following content to your `.env` file:

```bash
MAILGUN_SECRET_KEY=Some value
ANOTHER_APP_SECRET_KEY=Different_value
```
Now we are in a situation that we have a new file `.env` in our app and we need to avoid git publishing it. Run the `git status` command and you will notice that `git` sees `.env` as an untracked file:

```bash
git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

    .env

nothing added to commit but untracked files present (use "git add" to track)
```

We want `git` to totally ignore this file as it contains our secret keys. We do not want to commit and push them ever. Let's git ignore this file:

```bash
touch .gitignore
```
And add the `.env` file as a string in your `.gitignore` file, for guidance see this project [.gitgnore file](https://github.com/MirelaI/flask_heroku_example/blob/master/.gitignore). Now type `git status` again and you should see:

```
git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

    .gitignore

nothing added to commit but untracked files present (use "git add" to track)
```

From now on, `git` will have no idea about our `.env` file and we can go ahead and commit this change.

Your directory structure should be simmilar to:
```bash
.
├── .env
├── .gitignore
├── Procfile
├── README.md
├── app.py
├── requirements.txt
├── runtime.txt
└── templates
    └── index.html
```

Start the application again using `heroku local`

```bash
 heroku local
[OKAY] Loaded ENV .env File as KEY=VALUE Format
13:16:09 web.1   |   * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
13:16:09 web.1   |   * Restarting with stat
13:16:09 web.1   |   * Debugger is active!
13:16:09 web.1   |   * Debugger PIN: 782-892-076

```

Please note the __OKAY__ message. Heroku now reads our environment variables from the `.env` file and we just need to make use of them in our code. Amend `app.py` to read the mailgun secret key as an environemnt variable. In `app.py`, replace `mailgun_secret_key_value = None` with
`mailgun_secret_key_value = os.environ.get('MAILGUN_SECRET_KEY', None)`. Now your code should be:

```pyhon
import os
from flask import Flask, render_template

app = Flask('MyHerokuApp')

# ADJUSTMENT: Read the mailgun secret key from config variables
mailgun_secret_key_value = os.environ.get('MAILGUN_SECRET_KEY', None)

# This is needed for Heroku configuration as in Heroku our
# app will porbably not run on port 5000 as Heroku will automatically
# assign a port for our application
port = int(os.environ.get("PORT", 5000))

@app.route('/')
def index():

    # We will just display our mailgun secret key, nothing more.
    return render_template("index.html", value=mailgun_secret_key_value)
```

Since we started our application with `debug=True` any change to our code will trigger a restart in our application. After the application was restarted go in your browser and access http://localhost:5000/, the following should be displayed in your browser:

```
Value: Some value!
```
Another SUCCESS, our application now reads environment variables and we can use them to store out secret keys!

Please commit the changes and push them to heroku:

```
# Add the changes in staging area
git add .
# Commit with a meaningful message
git commit -am "Make use of environment variables"

# Deploy our changes to Heroku
git push heroku master
```

### Setup production environment variables
Since we deployed recently our Flask app to Heroku and the change included the make use of the environment variables, let's go and reload our heroku app in browser and see what happens. Access in your browser the Heroku URL that was provided to you when you run the `heroku create` command. In my case `https://murmuring-oasis-31169.herokuapp.com/`.
You should see:
```
No value defined!
```
And that is correct. We definded our variables in `.env` which is hidden from `git`, so Heroku has no idea about our newly defined variables. This means that we need to define our environment variables so that Heroku production environment, where our application is running, knows about them.

This is pretty simple, for every production environment varible that you want to define or update, you need to run from your terminal the following command, of course just replace the variable name and value:

```
heroku config:set SOME_SECRET_KEY=Some value
```

Let's go ahead and setup our `MAILGUN_SECRET_KEY` secret key:

```
heroku config:set MAILGUN_SECRET_KEY="Some value"
```

_Note: We need double quotes as the value contains whitespace, otherwise you do not need double quotes_

Reload your application in our browser and you should see:
```
Value: Some value!
```

You can see/edit/delete in Heroku dashboard all the environment variables that you defined so far. Go the [Heroku Dashboard](https://dashboard.heroku.com/apps), click on your application -> Settings -> Reveal Config Vars. You should see all environment vars defined so far. Here is my view:
![alt config vars](https://github.com/MirelaI/flask_heroku_example/blob/master/config_vars.png)

This is it! If you followed the steps as presented you should have an app running on Heroku that reads secret keys from environment varibles, which are hidden from Github.

**IMPORTANT: Now, please go ahead and delete your `/` route and `index()` method as users will be able to read your secret key if they know your application URL. This is just a basic example on how you can read configuration variables for different environments and by no means you want to expose this to the users.**

## Conclusion
These are the instructions needed to create a deployable Heroku application using Flask and environment variables. In short, make sure you add:
* `Procfile`
* `requirements.txt`
* `runtime.txt`

files to make your app deployable via Heroku.

In order to keep your secret keys hidden, for __local__ environment(your laptop) define a `.env` file where you put your keys, in a KEY=VALUE format, see [`.env_example`](https://github.com/MirelaI/flask_heroku_example/blob/master/.env_example)
file in this repo and then add it to the `.gitignore` file.

For __production__ environment, run the heroku command from your terminal (make sure you are in your project directory):
```
heroku config:set SOME_SECRET_KEY=Some value
```
or make use of the Heroku Dashboard.

This repository contains a full example of the steps above and the `app.py` contains an extra route to be able to interogate our configuration via our Flask app. Have a read through the code and let me know if you have any questions.

This example works perfectly if you already have a repository and just want to make it Heroku compatible, be sure you add the required files and your app should be deployable.

Happy coding!👩‍💻
