from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"


# index handler -- handler also called 'views' or 'controllers' 
# ~ function that responds to a specific event
@app.route("/") # responds to GET
def index(): 
    print "WHATH:LDFKJ:SLDF"
    return render_template("index.html")

@app.route("/", methods=["POST"]) # responds to POST
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")
    # flash is a function that takes in a string. Each string is queued in the flash,
    # waiting to be displayed only once.
    if model.authenticate(username, password):
        flash("User authenticated")
    else:
        flash('Password incorrect, there may be a ferret stampeded in progress!')
    return redirect(url_for("index"))

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug = True)
