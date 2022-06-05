import mysql.connector as mysql

mydb = mysql.connect(
  host="localhost",
  user="admin",
  password="admin",
  database='chatroom'
)


cur = mydb.cursor()
cur.execute("SELECT * FROM users")
r = cur.fetchall()
print(r)



def check_username(username):
    cur.execute("SELECT * FROM users WHERE username = '" + username + "'")
    r = cur.fetchall()
    if r:
        return True
    else:
        return False

def validate_login(username, password):
    cur.execute("SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'")
    r = cur.fetchall()
    if r:
        return True
    else:
        return False


def ADD_USER(username, password):
    if(not check_username(username)):
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mydb.commit()
        return True
    else:
        return False