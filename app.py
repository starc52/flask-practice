from flask import Flask, render_template, flash, redirect, request, url_for

import traceback, time, os

from models import *
from password_mgm import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = os.urandom(23)

db.init_app(app)

app.secret_key = os.urandom(27)

if not os.path.exists('logs'):
    os.makedirs('logs')

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.errorhandler(404)
def error404(e):
    return render_template("404.html")

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
        return render_template("error500.html", exp=exp, tried="rendering recents.htmls", tb="Trace back stored in logs")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['username']
        user_password = encrypt(request.form['password'])
        check_if_exists = User.query.filter_by(username= new_username).first()
        if check_if_exists:
            flash(f"Cannot create {new_username} already exists try a different user name")
            return render_template("register.html")
        try :
            new_user = User(username=new_username, password=user_password, loggedIn=0)
            db.session.add(new_user)
            db.session.commit()
            flash(f"{new_username} Successfully Created login go to Login page")
        except Exception as exp:
            tracebk = traceback.format_exc()
            logFile = open("logs/register_failed", 'a')
            log = f"Register Failed at {time.asctime()}\n\nException: {exp}\n\n{tracebk}\n\n\n"
            logFile.write(log)
            logFile.close()
            return render_template("error500.html", exp=exp, tried="registering", tb="Trace back stored in logs")


    return render_template("register.html")
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    # TODO Make one user not allow to login again by visiting login page while he is still logged in
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            query = User.query.filter_by(username= username).first()
            if not (query is None):
                if check(password, query.password):
                    query.loggedIn = 1
                    db.session.commit()
                    return redirect(url_for("dashboard", user=username))
                else:
                    flash("Username / Password incorrect Please check it")
            else:
                flash("Particular user Doesn't Exist")
            return render_template("login.html")
        except Exception as exp:
            tracebk = traceback.format_exc()
            logFile = open("logs/login_failed", 'a')
            log = f"Login Failed at {time.asctime()}\n\nException: {exp}\n\n{tracebk}\n\n\n"
            logFile.write(log)
            logFile.close()
            return render_template("error500.html", exp=exp, tried=f"logging in user - {username}", tb="Trace back stored in logs")
    
    return render_template("login.html")

@app.route("/dashboard/<user>/")
def dashboard(user):
    query = User.query.filter_by(username= user).first()
    if query:
        if query.loggedIn == 1:
            data = sacredText.query.filter_by(user= user)
            ids = []
            texts = []
            for x in data:
                ids.append(x.id)
                texts.append(x.text)
            return render_template("dashboard.html", user=user, text=texts, ids = ids)
        else:
            return render_template("dashboard.html")
    else:
        return render_template("404.html")

@app.route("/dashboard/addText/<user>/", methods=['GET', 'POST'])
def addText(user):
    if request.method == 'POST':
        text=request.form['text']
        try:
            new_text = sacredText(text=text, user=user)
            db.session.add(new_text)
            db.session.commit()
            flash("Successfully added the text")
        except Exception as exp:
            tracebk = traceback.format_exc()
            logFile = open("logs/addText_failed", 'a')
            log = f"addText Failed at {time.asctime()}\n\nException: {exp}\n\n{tracebk}\n\n\n"
            logFile.write(log)
            logFile.close()
            return render_template("error500.html", exp=exp, tried="addText", tb="Trace back stored in logs")
            
    return render_template("addText.html", user=user)

@app.route("/logout/<user>/")
def logout(user):
    # TODO Anyone can logout a User who is logged in, this should not be allowed
    query = User.query.filter_by(username= user).first()
    if query:
        query.loggedIn = 0
        db.session.commit()
        flash("Successfully Logged Out")
        return redirect(url_for('login'))
    else:
        return render("404.html")
    
@app.route("/allSacredTexts/<user>", methods=['GET', 'POST'])
def allSacredTexts(user):
    query = User.query.filter_by(username= user).first()
    if query:
        if query.loggedIn == 1:
            data = sacredText.query
            ids = []
            users = []
            texts = []
            edited = []
            for x in data:
                ids.append(x.id)
                texts.append(x.text)
                users.append(x.user)
                edited.append(x.edited)
            return render_template("allSacredTexts.html", user=user, text=texts, users=users, edited=edited, ids = ids)
        else:
            return render_template("allSacredTexts.html")
    else:
        return render_template("404.html")
        
@app.route("/edit/<id>/<user>", methods=['GET', 'POST'])
def edit(id, user):
    if request.method == 'POST':
        query = User.query.filter_by(username = user).first()
        if query:
            if query.loggedIn == 1:
                try:
                    new_text = request.form['newPost']
                    old_text = sacredText.query.filter_by(id = id).first()
                    old_text.text = new_text
                    db.session.commit()
                    flash(f"Changed Text")
                    return redirect(url_for("dashboard", user = user))
                except Exception as exp:
                    tracebk = traceback.format_exc()
                    logFile = open("logs/edit_failed", 'a')
                    log = f"edit Failed at {time.asctime()}\n\nException: {exp}\n\n{tracebk}\n\n\n"
                    logFile.write(log)
                    logFile.close()
                    return render_template("error500.html", exp=exp, tried="edit", tb="Trace back stored in logs")

            else:
                return render_template("404.html")
        else:
            return render_template("404.html")
    return render_template("edit.html", id = id, user = user)

@app.route("/dashboard/delete/<id>/<user>")
def delete(id, user):
    query = User.query.filter_by(username = user).first()
    if query:
        if query.loggedIn == 1:
            try:
                if not sacredText.query.filter_by(id = id).first():
                    return render_template("404.html")
                sacredText.query.filter_by(id = id).delete()
                db.session.commit()
                flash(f'Deleted')
                return redirect(url_for("dashboard", user = user))
            except Exception as exp:
                tracebk = traceback.format_exc()
                logFile = open("logs/edit_failed", 'a')
                log = f"edit Failed at {time.asctime()}\n\nException: {exp}\n\n{tracebk}\n\n\n"
                logFile.write(log)
                logFile.close()
                return render_template("error500.html", exp=exp, tried="edit", tb="Trace back stored in logs")
        else:
            return render_template("404.html")
    else:
        return render_template("404.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)