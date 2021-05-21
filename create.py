import sqlite3

con = sqlite3.connect('data.db')
cursor = con.cursor()
create_user_query = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,username TEXT,password TEXT)"
create_item_query = "CREATE TABLE IF NOT EXISTS items(name TEXT, price REAL)"

row = cursor.execute(create_user_query)
row = cursor.execute(create_item_query)
# query = "SELECT * FROM items"
# row = cursor.execute(query)
# for r in row:
#     print(r)
con.close()