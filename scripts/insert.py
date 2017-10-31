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
    'user': 'kherring',
    'password': '12faye',
    'host': '127.0.0.1',
    'database': 'rwandanlaw'
}

form = cgi.FieldStorage()

data = {
 'username': form.getvalue('username')
 'first_name': form.getvalue('first_name')
 'last_name': form.getvalue('last_name')
 'email': form.getvalue('email')
 'password': form.getvalue('password')
 'repeated_password': form.getvalue('repeated_password')
}

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
