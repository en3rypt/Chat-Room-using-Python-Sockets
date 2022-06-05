import mysql.connector as mysql
from datetime import datetime

mydb = mysql.connect(
  host="localhost",
  user="admin",
  password="admin",
  database='chatroom'
)


cur = mydb.cursor()

def storeMessaage(username,message):
    sql = f"INSERT INTO chatLog (username,date,message) VALUES('{username}','{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}','{message}')"
    cur.execute(sql)
    mydb.commit()
def getMessage():
    cur.execute("SELECT * FROM chatLog")
    r = cur.fetchall()
    return r




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