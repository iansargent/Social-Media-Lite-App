'''
Ian Sargent
CS 2500
Social Media App
'''
# Necessary packages
import pwinput as pw
import sqlite3
from datetime import datetime


# Setting the database connection and the cursor
con = sqlite3.connect("social_media.db")
cur = con.cursor()


# Function for user login
def login():
    valid_check = None
    while valid_check is None:
        # Welcome message to begin
        print("Welcome to Social Media Lite")
        
        # Get the username and password from the user
        username = input("Username: ")
        password = pw.pwinput(prompt="Password: ")
        # Set inputs as parameters for the SQLite query
        login_params = (username, password)

        # Execute the query and save it
        in_db = cur.execute('''
                            SELECT * FROM Users 
                            WHERE username = ? AND password = ?
                            ''', login_params)

        # Check if the result of the query is True or False
        valid_check = in_db.fetchone()

        # If user is not found in the database . . .
        if valid_check is None:
            print("User not found. Please try again.")
    
    print("Successful login!")
    return username, password


# Function for the user info section
def handle_user_info(login_params):
    # Retrieving user info for that specific user
    user_info = cur.execute('''
                            SELECT username, account_created, first_name, last_name, birth_date 
                            FROM Users WHERE username = ? AND password = ?
                            ''', login_params).fetchone()

    # Display the information
    print(f"Username: {user_info[0]}\n" +
          f"Account Created: {user_info[1]}\n" +
          f"First Name: {user_info[2]}\n" +
          f"Last Name: {user_info[3]}\n" +
          f"Date of Birth: {user_info[4]}\n")

    # Boolean flag
    user_info_flag = True
    # Loop for editing user information
    while user_info_flag:
        # Given option of editing or returning to main screen
        info_choice = input("Choose an option\na) Go back\nb) Edit\n=> ")

        # Edit User Info chosen
        if info_choice == "b":
            print(f"Available columns: ")
            # Define available columns for input validation
            available_columns = ["email_id", "password", "first_name", "last_name", "birth_date"]

            # Show the available columns
            for column in available_columns:
                print(column)

            # Boolean flag
            edit_flag = True
            # Loop in case they want to edit multiple fields
            while edit_flag:
                # Retrieving the column they would like to edit
                edit_column = input("Which column would you like to edit? ")

                # Ensuring column is in the list of available ones to edit
                if edit_column in available_columns:
                    # Exit the edit loop
                    edit_flag = False
                    # Retrieving the new value for the specified column
                    user_edit = input(f"What would you like to set {edit_column} to? ")
                    # Query to update that value in the database
                    cur.execute(f'''
                                UPDATE Users SET {edit_column} = ? 
                                WHERE username = ? AND password = ?;
                                ''', (user_edit, login_params[0], login_params[1]))
                    con.commit()
                
                else:
                    print("That is not an available column. Please try again.")

        elif info_choice == "a":
            print("Going back to the previous menu.")
            user_info_flag = False

        else:
            print("That is not an available option. Please try again.")


# Function for the posts section
def handle_posts(user_id, username, password):
    print("Posts:")
    # SQLite query to retreive all posts from that user
    posts = cur.execute('''
                        SELECT posted_date, post 
                        FROM Posts INNER JOIN Users ON Posts.user_id = Users.user_id
                        WHERE username = ? AND password = ?
                        ORDER BY posted_date
                        ''', (username, password)).fetchall()
            
    # If the user has posted (not empty)
    if posts:
        # Loop through all posts and display them (formatted --> "date: post")
        for post in posts:
            print(f"{post[0]}: {post[1]}")
            
    # If the user has not posted
    else:
        print("You have no posts yet.")
            
    # Boolean flag
    post_flag = True       
    # Loop for creating posts
    while post_flag:    
        # Option given to return or add a post
        post_choice = input("Choose an option\na) Go back\nb) Add post\n=> ")
        
        # If they want to add a post
        if post_choice == "b":       
            # Retrieve the post content
            new_post = input("Type new post: ")       
            # Defining the current date with the datetime package
            current_date = datetime.now().strftime("%m/%d/%Y")      
            # SQLite query to insert the new post for that user on the current date
            cur.execute('''
                        INSERT INTO Posts (user_id, post, posted_date)
                        VALUES (?, ?, ?);
                        ''', (user_id, new_post, current_date))
            # Commit changes to the database
            con.commit()
                
        # Returning to the main menu
        elif post_choice == "a":
            print("Going back to the previous menu.")
            # Exit post loop
            post_flag = False

        # Input validation (not 'a' or 'b')
        else:
            print("That is not a valid option. Please try again.")


# Function for the follow section
def handle_follow(user_id):
    print("Followers: ")

    # SQLite query to retrieve all a user's followers
    followers = cur.execute('''
                            SELECT Users.first_name, Users.last_name
                            FROM Followers
                            INNER JOIN Users ON Followers.follow_id = Users.user_id
                            WHERE Followers.user_id = ?
                            ''', (user_id,)).fetchall()
            
    # Display those followers
    for follower in followers:
        print(f"{follower[0]} {follower[1]}")

    # Boolean flag
    follow_flag = True       
    # Loop for following another user
    while follow_flag:   
        # Add a follower or return to the main menu
        follow_choice = input("Choose an option\na) Go back\nb) New follow\n=> ")

        # Add a follower selected
        if follow_choice == "b":     
            print("People not following: ")
            
            # SQLite query to retrieve all other users that they do not follow yet
            not_following = cur.execute('''
                                        SELECT first_name, last_name, user_id
                                        FROM Users
                                        WHERE user_id != ? AND user_id NOT IN
                                        (SELECT follow_id FROM Followers WHERE user_id = ?)
                                        ''', (user_id, user_id)).fetchall()

            ids_not_followed = []
            # Loop through users not following
            for user in not_following:
                # Store a list of user_ids not followed (for input validation)
                ids_not_followed.append(user[2])
                # Formatted display of first name, last name, and user ID
                print(f"{user[0]} {user[1]}, User ID: {user[2]}")

            # Retrieve ID of the user they would like to follow
            id_to_follow = input("ID of person to follow: ")

            try:
                # Ensure user_id is an integer
                id_to_follow = int(id_to_follow)
                        
                # If valid user_id given
                if id_to_follow in ids_not_followed:        
                    # SQLite query to add that follow relationship into the database
                    cur.execute('''
                                INSERT INTO Followers (user_id, follow_id)
                                VALUES (?, ?);
                                ''', (user_id, id_to_follow))
                    # Commit the changes to the database
                    con.commit()
                    # Success message when completed
                    print("Follow successful!")
                
                # If they already follow that ID or ID is not found in the database
                else:
                    print("You already follow that user or ID was not found.")

            # If they enter anything besides an integer
            except ValueError:
                print("Invalid input. Please enter a valid user ID.")
        
        # Returning to the main menu
        elif follow_choice == "a":
            print("Going back to the previous menu.")
            # Exit the follow loop
            follow_flag = False
                
        # Input validation (Not 'a' or 'b')
        else:
            print("That is not a valid option. Please try again.")


# The main program 
def main():
    # Loop
    while True:
        # Retrieve username and password
        username, password = login()
        # Define login params (tuple)
        login_params = (username, password)
        # Retrieve the user's user_id number
        user_id = cur.execute('''
                              SELECT user_id FROM Users
                              WHERE username = ? AND password = ?
                              ''', login_params).fetchone()[0]
        # Boolean flag
        master_flag = True
        # Master loop (to return to main menu)
        while master_flag:
            # Retrive the user's main menu option
            master_choice = input("a) User info\nb) Posts\nc) Follow\nd) Log-out\n=> ")

            # User info selected
            if master_choice == "a":
                handle_user_info(login_params)

            # Posts selected
            elif master_choice == "b":
                handle_posts(user_id, username, password)
            
            # Follow selected
            elif master_choice == "c":
                handle_follow(user_id)
            
            # Log out selected
            elif master_choice == "d":
                print("Logging out ...")
                master_flag = False

            # Invalid choice (not 'a', 'b', 'c', or 'd')
            else:
                print("That is not a valid option. Please try again.")


# Running the program
if __name__ == "__main__":
    main()
