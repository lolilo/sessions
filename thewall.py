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
    query = """SELECT * FROM ?"""
    DB.execute(query, (table,))
    rows = DB.fetchall()
    return rows

# look up user's id by their name
def get_user_by_name(username):
    query = """SELECT id FROM users WHERE username=?"""
    print 'USERNAME', username
    print ''
    
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
    print "Successfully added wall post."

def main():
    connect_to_db()
    command = None
    while command != "quit":

        input_string = raw_input("TheWall Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "table":
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

        # if command == "student":
        #     get_student_by_github(*args) 
        # elif command == "new_student":
        #     make_new_student(*args)
        # elif command == "project_title":
        #     get_project_by_title(*args)
        # elif command == "new_project":
        #     # need to format for string as second argument 
        #     title = args[0]
        #     desc = ' '.join(args[1:-1]) 
        #     max_grade = args[-1]  
        #     make_new_project(title, desc, max_grade)
        # elif command == "get_grade":
        #     get_grade_by_project(*args)
        # elif command == "assign_grade":
        #     give_grade_to_student(*args)  
        # elif command == "show_student_grades":
        #     show_all_grades_for_student(*args)      


    CONN.close()

if __name__ == "__main__":
    main()