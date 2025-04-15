'''
Ian Sargent
CS 2500
Social Media App

Inserting birth date values
'''

# Necessary package
import sqlite3

# Setting the database connection and the cursor
con = sqlite3.connect("social_media.db")
cur = con.cursor()

# Defining the birth date values
birth_dates = ["10/18/1999", "8/19/1998", "9/29/2001", "11/26/1995", "10/22/2002", "12/22/1999", "10/5/2000", "1/3/2003"]

# Adding the new birth_date column to the Users table
cur.execute('''
ALTER TABLE Users
ADD COLUMN birth_date TEXT;
''')

# Looping through each birth date and inserting it with each user_id value (1 - 8)
for i, date in enumerate(birth_dates):
    cur.execute(f'''
    UPDATE Users
    SET birth_date = '{date}'
    WHERE user_id = {i + 1};
    ''')

# Commit the changes and close the connection
con.commit()
con.close()