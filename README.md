# Social Media Lite
CS 2500 – Python and SQLite Project

## 📝 Description
A command-line social media application built in Python that allows users to:

- Log in with a username and password  
- View and edit their profile information  
- Create and view posts  
- Follow other users

All data is stored using an SQLite database.

#### Skills Developed
- Connecting to a SQLite database and querying it using Python
- Implementing user authentication with input validation and error handling

## 📂 Files
#### Python Scripts
- **csv_to_sqlite.py** – A script that uploads the three provided CSV files into a created database file ('social_media.db')
- **birth_dates.py** – A script that adds a date of birth column into a table in the previously created database
- **social_media_lite.py** – The main script with a login system and available user actions

#### CSVs
- **users.csv** — Contains account details for all users (e.g., usernames, names, birth dates)
- **posts.csv** — Stores each post along with the user ID of the person who posted it
- **followers.csv** — Lists user relationships by pairing each user with their followers' IDs

## 💾 Dependencies
- *pwinput* module  
  ```bash
  pip install pwinput
  
- *sqlite3* module  
  ```bash
  pip install sqlite3

- *datetime* module  
  ```bash
  pip install datetime
