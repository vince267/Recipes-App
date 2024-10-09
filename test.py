import argon2
# https://argon2-cffi.readthedocs.io/en/stable/api.html
import sqlite3

ph = argon2.PasswordHasher()


# print(truefalse)



# Create connection to database 
con = sqlite3.connect("recipes.db")

# Create cursor object 
cur = con.cursor()



# Query database for username
# rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
result = cur.execute("SELECT id, username, hash FROM users WHERE username = ?", ('vince',))
# result = cur.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
rows = result.fetchall()

print(rows)
print(len(rows))
# # Ensure username exists
# if len(rows) !=1: 
#     print("username dne")

