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
    username = request.form.get("username")
    password = request.form.get("password")
    # flash is a function that takes in a string. Each string is queued in the flash,
    # waiting to be displayed only once.

    user_id = model.authenticate(username, password)
    thewall.connect_to_db()

    if username != None:
        flash("User authenticated!")
        session['username'] = user_id # put user_id into the session rather than username
    else:
        flash('Password incorrect, there may be a ferret stampeded in progress!')

    return redirect(url_for("index"))

# The handler should take the username passed to it, and look up the user's id by their name.
@app.route("/user/<username>")
def view_user(username):
    thewall.connect_to_db()
    user_id = thewall.get_user_by_name(username)
    # Use that id to look up that user's wall_posts, then send the collection of rows to a template named wall.html.
    wall_posts = thewall.get_wall_posts_by_user_id(user_id)
    html = render_template('wall.html', owner_id = username, wall_posts = wall_posts, author_name = username)

    return html

# It will receive the text from handler number one, /user, extract a username from the url, 
# and extract the user id of the currently logged-in user from the session.
@app.route("/post_to_wall/<username>", methods=["POST"])
def post_to_wall(username):
    # username = request.args.get("username") # it gets this from the URL
    owner_id = thewall.get_user_by_name(username) # user_id

    logged_in_user = session.get('username') # currently logged-in user
    author_id = thewall.get_user_by_name(logged_in_user) # currently logged-in user
    content = request.form.get("content")

    if content != None:
        thewall.new_wall_post(owner_id, author_id, content)
    return redirect(url_for("view_user", username=username))

# clear session
@app.route("/logout")
def clear_session():
    session.clear()
    return redirect(url_for('index'))

@app.route("/register")
def register():
    if session.get('username'):
        username = session.get('username')
        return redirect(url_for("view_user", username=username))
    else: 
        return redirect(url_for("create_account"))

@app.route("/create_account")
def create_account():
    if session.get('username'):
        return redirect(url_for("register"))
    else: 
        html = render_template('register.html')
        return html

@app.route("/create_account", methods=["POST"])
def process_create_account():
    thewall.connect_to_db()

    username = request.form.get("username")
    password = request.form.get('password')
    new_user_created = thewall.new_user(username, password)

    if new_user_created:
        flash('New account successfully registered! Please log in.')
        return redirect(url_for("index"))
    else: 
        flash('Sorry, that username is already registered. Please try another.')
        return redirect(url_for("register"))
    # If they do exist, flash an error message and redirect them to the register page.
    # If they don't exist, create a new record for them in the database, 
    # flash a message saying their user was created, then redirect them to the login page.

if __name__ == "__main__":
    app.run(debug = True)
