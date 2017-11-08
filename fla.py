# insert.py
# Create all tables in the Rwandan Law database
# Group: Ctructure
# Date: 10/30/2017

import mysql.connector as mc
from mysql.connector import errorcode
import sys
from flask import Flask,render_template, json, request
app = Flask(__name__)
 
@app.route("/")
def hello():
    return "Hello World!"
 
if __name__ == "__main__":
    app.run()


@app.route('/login',methods = ['GET'])
def get_login():
   #define user connection
    config = {
        'user': 'kherring',
        'password': '12faye',
        'host': '127.0.0.1',
        'database': 'rwandanlaw'
    }

    data = {
     'username': request.form('username')
     'first_name': request.form('first_name')
     'last_name': request.form('last_name')
     'email': request.form('email')
     'password': request.form('password')
     'repeated_password': request.form('repeated_password')
    }

    return json.dumps(data)


    # build query
    placeholders = ', '.join(['%s'] * len(data))
    cols = ', '.join(data.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s%s )" % ('users', cols, data.values(), placeholders)

    try:
        cnx = mc.connect(**config)
        cursor = cnx.cursor()
        cursor.execute(sql)

    except mc.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print "Err: Access Denied (Verify user and password)"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print "Database not found"
        else:
            print err
        sys.exit(1)

if __name__ == '__main__':
   app.run()