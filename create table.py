import sqlite3

# Create a connection to the database
conn = sqlite3.connect('treeDB.db')

# Create a cursor object
cursor = conn.cursor()

# Create the `tree` table
cursor.execute('CREATE TABLE IF NOT EXISTS tree ('
               'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               'full_name VARCHAR(255),'
               'maiden_name VARCHAR(255),'
               'born_date DATE,'
               'death_date DATE,'
               #'father INT,'
               #'mother INT,'
               #'children INT,'
               'source_link VARCHAR(255)'
               ')')

# Commit the changes
conn.commit()



# Create the `relationships` table
cursor.execute('CREATE TABLE IF NOT EXISTS relationships ('
               'id INTEGER PRIMARY KEY AUTOINCREMENT,'
               'parent_id INT,'
               'child_id INT,'
               'FOREIGN KEY(parent_id) REFERENCES tree(id),'
               'FOREIGN KEY(child_id) REFERENCES tree(id)'
               ')')

# Commit the changes
conn.commit()

# Close the connection
conn.close()
