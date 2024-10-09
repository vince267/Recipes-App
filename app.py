import argon2 # https://argon2-cffi.readthedocs.io/en/stable/api.html
# from _argon2_cffi_bindings import ffi, lib
import os
import sqlite3
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import apology, login_required

# If flask server gives "Access Denied" -> chrome://net-internals/#sockets -> Flush socket pools
# Get flashed messages https://flask.palletsprojects.com/en/2.2.x/patterns/flashing/


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Secure password hasher from argon2 - https://argon2-cffi.readthedocs.io/en/stable/api.html
ph = argon2.PasswordHasher()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required



def index():
    """To Do"""
    # return redirect("/login")
    # return apology("DOG?", 403)

    # Create connection to databate
    con = sqlite3.connect("recipes.db")
    # Create cursor object 
    cur = con.cursor()

    res = cur.execute("SELECT name, id FROM recipes WHERE userid = ?", (session["user_id"],))
    data = res.fetchall()

    cur.close()
    con.close()

    return render_template("index.html", data=data)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add recipe"""

    if request.method == "POST":
        # First make sure that the user hasn't already added a recipe with that name yet. If that happens, render an apology.
        if not request.form.get("name"):
            return apology("Must provide a recipe name", 403)

        # Next make sure the user filled out the ingredients, amounts, units, and steps forms. If not, render an apology. 
        if not request.form.getlist("ingredients[]"):
            return apology("Must provide a list of ingredients", 403)
        
        if not request.form.getlist("amounts[]"):
            return apology("Must provide amounts of ingredients", 403)

        if not request.form.getlist("units[]"):
            return apology("Must provide units for ingredients", 403)

        if not request.form.getlist("steps[]"):
            return apology("Must provide steps for the recipe", 403)        
            

        # Get posted info into variables
        ingredients = request.form.getlist("ingredients[]")
        amounts = request.form.getlist("amounts[]")
        units = request.form.getlist("units[]")
        steps = request.form.getlist("steps[]")
        comments = request.form.get("comments")
        recipe_name = request.form.get("name")
        time = datetime.now()

        # Create connection to database 
        con = sqlite3.connect("recipes.db")
        # Create cursor object 
        cur = con.cursor()

        # # Plan: we have userid already. Get the recipe name from the post request and add it to the recipes table. Include date and time
        cur.execute("INSERT INTO recipes (name, comments, userid, datetime) VALUES(?, ?, ?, ?)", (recipe_name, comments, session["user_id"], time))
        # recipeid = cur.execute("SELECT id FROM recipes WHERE name = ? AND comments = ? AND userid = ? AND datetime = ?)", (recipe_name, comments, 5, time))
        res = cur.execute("SELECT id FROM recipes WHERE name = ? AND comments = ? AND userid = ? AND datetime = ?", (recipe_name, comments, session["user_id"], time))
        list = res.fetchone()
        recipeid = int(list[0])

        if not recipeid:
            return apology("An error has occured", 403)


        # Format recipe data to insert into database
        recipe_data = []
        for i in range(len(ingredients)):
            recipe_data.append((ingredients[i], amounts[i], units[i], recipeid))

        # here we will add each ingredient, amount, and unit.
        cur.executemany("INSERT INTO ingredients VALUES(?, ?, ?, ?)", recipe_data) 
         
        step_data = []
        for step in steps:
            step_data.append((step, recipeid)) 

        cur.executemany("INSERT INTO steps VALUES(?, ?)", step_data)

        con.commit()
        cur.close()
        con.close()




        return redirect("/")

    else:
        return render_template("add.html")




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    
    # Create connection to database 
    con = sqlite3.connect("recipes.db")

    # Create cursor object 
    cur = con.cursor()



    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        result = cur.execute("SELECT id, username, hash FROM users WHERE username = ?", (request.form.get("username"),))
        # result = cur.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        rows = result.fetchall()

        # Ensure username exists
        if len(rows) !=1: 
            return apology("invalid username", 403)

        # Ensure password is correct
        try:
            ph.verify(rows[0][2], request.form.get("password"))

        # In case password verification raises exception
        except: 
            return apology("Invalid password", 403)

        # Password was verified. Check if password needs to be rehashed. 
        if ph.check_needs_rehash(ph.hash(request.form.get("password"))):
            cur.execute("UPDATE users SET hash = ? WHERE username = ?", (ph.hash(request.form.get("password")), request.form.get("username")))
            con.commit()
            # db.set_password_hash_for_user(user, ph.hash(password))
        
        cur.close()
        con.close()

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/recipe", methods=["POST"])
def recipe():

    if request.method == "POST":
        

        id = request.form.get("id")
        name = request.form.get("name")
        # Need to pass in all the receipe data so it can be displayed in recipe.html. 

        # Create connection to database 
        con = sqlite3.connect("recipes.db")
        # Create cursor object 
        cur = con.cursor()

        # Get all recipe data using recipe id

        res1 = cur.execute("SELECT comments, datetime FROM recipes WHERE id = ? AND userid = ?", (id, session["user_id"]))
        recipes = res1.fetchone()

        res2 = cur.execute("SELECT ingredient, amount, unit FROM ingredients WHERE recipeid = ?", (id,))
        ingredients = res2.fetchall()

        res3 = cur.execute("SELECT steps FROM steps WHERE recipeid = ?", (id,))
        steps = res3.fetchall()



        # Close all connections
        cur.close()
        con.close()


        # Redirect user to login form
        return render_template("recipe.html", name=name, recipes=recipes, ingredients=ingredients, steps=steps)

    else:
        return apology("How did you get here...?", 403)



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Create connection to database 
    con = sqlite3.connect("recipes.db")

    # Create cursor object 
    cur = con.cursor()


    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Query database for username
        result = cur.execute("SELECT username FROM users WHERE username = ?", (request.form.get("username"),))

        rows = result.fetchall()

        if len(rows) != 0:
            return apology("username already exists", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        hashed = ph.hash(request.form.get("password")) # argon2 hash
        cur.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (request.form.get("username"), hashed))
        con.commit()

        return redirect("/login")

    else:
        return render_template("register.html")
