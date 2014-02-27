import sqlite3
import datetime

DB = None
CONN = None

# id          username    password  
# ----------  ----------  ----------
# 1           lilo        pass      
# 2           liana       pass      
# 3           hackbright  unicorn   
# 4           happy       unicorn   


# id          owner_id    author_id   created_at  content                    
# ----------  ----------  ----------  ----------  ---------------------------
# 2           1           1           12/12/12    This is my first wall post.
# 3           1           1           12/12/12    This is my second wall post
# 4           1           1           12/12/12    This is my third wall post.
# 5           1           1           12/12/12    This is my third wall post.
# 6           2           2           2014-02-26  sdlkfj sdglj               
# 7           2           1           2014-02-26  this is a weird post  


# users:
# id - int, primary key
# username - varchar
# password - varchar

# wall_posts:
# id - int, primary key
# owner_id - int (refers to users.id) -- not redundant!
# author_id - int (refers to users.id)
# created_at - datetime
# content - text

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

# ASK!!! CAN I NOT DO THIS? 
def show_table(table):
    print "in show_table"
    # DANGER WILL ROBINSON DON'T DO THIS
    # should validate user input via alphabet check or dictionary of valid table names
    query = """SELECT * FROM `%s`""" % table
    DB.execute(query)
    rows = DB.fetchall()
    return rows

# look up user's id by their name
def get_user_by_name(username):
    query = """SELECT id FROM users WHERE username=?"""
    DB.execute(query, (username,))
    row = DB.fetchone()

    return row[0]

# return rows of wall posts
def get_wall_posts_by_user_id(user_id):
    query = """SELECT * FROM wall_posts WHERE owner_id=?"""
    DB.execute(query, (user_id,))
    rows = DB.fetchall()
    return rows
    # We could also make this a dictionary. 

def new_wall_post(owner_id, author_id, content):
    query = """INSERT INTO wall_posts (owner_id, author_id, created_at, content) VALUES (?, ?, ?, ?)"""
    time_unformatted = datetime.datetime.now()
    # time = time_unformatted.strftime('%c')
    # print time
    DB.execute(query, (owner_id, author_id, time_unformatted, content))
    CONN.commit()
    print "Successfully added wall post to TABLE wall_posts."

def new_user(username, password):
    check_if_user_exists_query = """SELECT * from users WHERE username=?"""

    print 'USERNAME!', username
    print 'PASSOWRD', password
    print ''

    DB.execute(check_if_user_exists_query, (username,))
    existing_username = DB.fetchone()
    # print existing_username

    if existing_username != None:
        # return "That username is already taken."
        return False
    else: 
        query = """INSERT INTO users (username, password) VALUES (?,?)"""
        DB.execute(query, (username, password))
        CONN.commit()
        # return "Successfully added new user to TABLE users."
        return True

def main():
    connect_to_db()
    command = None
    while command != "quit":

        input_string = raw_input("TheWall Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        print command
        if command == "table":
            print "run show table"
            print show_table(*args)
        elif command == "username":
            print get_user_by_name(*args)
        elif command == "wall_posts":
            print get_wall_posts_by_user_id(*args)
        elif command == "new_wall_post":
            owner_id = args[0] # user_id associated with username
            author_id = args[1] # currently logged-in user
            content = ' '.join(args[2:])
            new_wall_post(owner_id, author_id, content)
        elif command == "new_user":
            username = args[0]
            password = args[1]
            print new_user(username, password)

    CONN.close()

if __name__ == "__main__":
    main()