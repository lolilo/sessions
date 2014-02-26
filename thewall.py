import sqlite3

DB = None
CONN = None

def get_user_by_name(username):
    query = """SELECT id FROM users JOIN wall_posts ON wall_posts.owner_id=users.id 
        WHERE users.username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    return row


def main():
    connect_to_db()
    command = None
    while command != "quit":

        input_string = raw_input("TheWall Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "username":
            get_user_by_name(*args)

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