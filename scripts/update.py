# insert.py
# Create all tables in the Rwandan Law database
# Group: Ctructure
# Date: 10/30/2017

import mysql.connector as mc
from mysql.connector import errorcode
import sys
import cgi

#define user connection
config = {
    'user': 'sdai2',
    'password': '111',
    'host': '127.0.0.1',
    'database': 'rwandanlaw'
}

form = cgi.FieldStorage()

data = {
 'email': form.getvalue('email')
 'password': form.getvalue('password')
 'repeated_password': form.getvalue('repeated_password')
}

# build query
username = 'test_id'
sql = "UPDATE %s SET email=%s, password=%s WHERE username = %s " % ('users', data['email'], data['password'], username)


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
