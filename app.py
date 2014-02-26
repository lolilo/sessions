from flask import Flask, render_template, request, redirect, session, url_for, flash
import model
import thewall

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"


# index handler -- handler also called 'views' or 'controllers' 
# ~ function that responds to a specific event

@app.route("/") # responds to GET
def index(): 
    if session.get('username'):
        return 'User %s is logged in!' % session['username']
    else: 
        return render_template("index.html")





@app.route("/", methods=["POST"]) # responds to POST. SUPER IMPORTANT!!!!!!!! PAY ATTENTION!
# change method = "POST" on html file
def process_login():
    user_id = request.form.get("username")
    password = request.form.get("password")
    # flash is a function that takes in a string. Each string is queued in the flash,
    # waiting to be displayed only once.
    # username = model.authenticate(username, password)

    thewall.connect_to_db()

    if username != None:
        flash("User authenticated!")
        session['username'] = user_id # put user_id into the session rather than username
    else:
        flash('Password incorrect, there may be a ferret stampeded in progress!')
    return redirect(url_for("index"))


@app.route("/user")
def view_user():
    thewall.connect_to_db()
    user_id = request.args.get("user_id")
    user = get_user_by_name(user_id)
    html = render_template('wall.html', user_id = user)

# need to clear session
@app.route("/logout")
def clear_session():
    session.clear()
    return redirect(url_for('index'))

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug = True)
