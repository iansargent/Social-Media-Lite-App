'''
Ian Sargent
CS 2500
Social Media App

Loading CSVs onto a SQLite database
'''

# Necessary packages
import sqlite3
import pandas as pd

# Setting the database connection and the cursor
con = sqlite3.connect("social_media.db")
cur = con.cursor()

# Uploading the "users" table
users = pd.read_csv('users.csv')
users.to_sql('Users', con, if_exists = 'append', index = False)

# Uploading the "followers" table
followers = pd.read_csv('followers.csv')
followers.to_sql('Followers', con, if_exists = 'append', index = False)

# Uploading the "posts" table
posts = pd.read_csv('posts.csv')
posts.to_sql('Posts', con, if_exists = 'append', index = False)
