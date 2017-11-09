## Create a tables

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'rwandanlaw'
TABLES = {}

TABLES['publications'] = (
  "CREATE TABLE `publications` ("
  "  `var_num` varchar(10) NOT NULL,"
  "  `name` varchar(55) NOT NULL,"
  "  `pub_date` date NOT NULL,"
  "  PRIMARY KEY(`var_num`, `pub_date`)"
  ") ENGINE=InnoDB")

TABLES['agencies'] = (
  "CREATE TABLE `agencies` ("
  "  `abbrev` varchar(15) NOT NULL,"
  "  `long_name` varchar(255) NOT NULL,"
  "  PRIMARY KEY (`abbrev`)"
  ") ENGINE=InnoDB")

cnx = mysql.connector.connect(user='amucungu', password='m90753',
                              host='localhost',
                              database='rwandanlaw')

cursor = cnx.cursor()

for name, ddl in TABLES.iteritems():
    try:
        print "Creating table {}: ".format(name)
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
