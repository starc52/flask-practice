from flask import Flask, render_template, flash, redirect, request

import traceback, time, os

from models import *
from password_mgm import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = os.urandom(23)

db.init_app(app)

keyfile = open("key.bin")
app.secret_key = keyfile.read()

if not os.path.exists('logs'):
    os.makedirs('logs')

@app.route("/")
def index():
    return render_template("index.html")

@app.errorhandler(404)
def error404(e):
    return render_template("404.html", e=e)

@app.route("/recents")
def recents():
    recent_ones = ['List1', 'List2', 'List3', 'List4', 'List5']
    # recent_ones = 3 # Creates internal server error 500, Checkout why by visiting page
    try:
        return render_template("recents.html", recent=recent_ones)
    except Exception as exp :
        # Save to logs
        tracebk = traceback.format_exc()
        logFile = open("logs/render_failed", 'a')
        log = f"Render Failed at {time.asctime()}\n\nException: {exp}\n\n{tracebk}\n\n\n"
        logFile.write(log)
        logFile.close()
        return render_template("error500.html", exp=exp, tried="rendering recents.htmls", tb=tracebk)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['username']
        user_password = encrypt(request.form['password'])
        try :
            new_user = User(username=new_username, password=user_password)
            db.session.add(new_user)
            db.session.commit()
            flash(f"{new_username} Successfully Created hashed password is {new_user.password}")
        except Exception as e:
            return render_template("exception.html", exp=e)

    return render_template("register.html")
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)