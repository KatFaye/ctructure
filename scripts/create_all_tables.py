# create_all_tables.py
# Create all tables in the Rwandan Law database
# Group: Ctructure
# Date: 10/28/2017

import mysql.connector as mc
from mysql.connector import errorcode
import sys

#define user connection
config = {
    'user': 'kherring',
    'password': '12faye',
    'host': '127.0.0.1',
    'database': 'rwandanlaw'
}

tables = {}
tables['agencies'] = (
  "CREATE TABLE `agencies` ("
  "  `abbrev` varchar(15) NOT NULL,"
  "  `long_name` varchar(255) NOT NULL,"
  "  PRIMARY KEY (`abbrev`)"
  ") ENGINE=InnoDB")

tables['articles']=(
   """CREATE TABLE articles (
   law char(10) NOT NULL,
   article_num int NOT NULL,
   text varchar(5000) NOT NULL,
   name varchar(500) NOT NULL,
   PRIMARY KEY (law,article_num),
   FOREIGN KEY (law)
   REFERENCES laws (law_num)
   )
"""
)

tables['cites'] = (
    """CREATE TABLE cites (
     parent_law varchar(35) NOT NULL,
     cited_law varchar(35) NOT NULL,
     INDEX (parent_law, cited_law),
     FOREIGN KEY (parent_law)
     REFERENCES laws(law_num),
     FOREIGN KEY (cited_law)
     REFERENCES laws(law_num)
    )
    """
)

tables['content_type'] = (
    "CREATE TABLE `content_type` ("
    "  `name` varchar(35) PRIMARY KEY,"
    "  `authority` int NOT NULL"
    ")")

tables['laws'] = (
    "CREATE TABLE `laws` ("
    "  `law_num` varchar(35) PRIMARY KEY ,"
    "  `name` varchar(500) NOT NULL,"
    "  `ending` varchar(500) ,"
    "  `publication` varchar(65) NOT NULL,"
    "  `intro` varchar(5000) NOT NULL,"
    "  `content_name` varchar(35) NOT NULL REFERENCES contents(content_type) ,"
    "  `publication_date` date NOT NULL REFERENCES publications(pub_date),"
    "  `publication_var_num` varchar(10) NOT NULL REFERENCES publications(var_num),"
    "  `agency` varchar(15) NOT NULL REFERENCES agencies(abbrev) "
    ")")

tables['publications'] = (
  "CREATE TABLE `publications` ("
  "  `var_num` varchar(10) NOT NULL,"
  "  `name` varchar(55) NOT NULL,"
  "  `pub_date` date NOT NULL,"
  "  PRIMARY KEY(`var_num`, `pub_date`)"
  ") ENGINE=InnoDB")

tables['repeals'] = (
    """CREATE TABLE repeals (
     parent_law varchar(35) NOT NULL,
     impacted_law varchar(35) NOT NULL,
     INDEX (parent_law, impacted_law),
     FOREIGN KEY (parent_law)
     REFERENCES laws(law_num),
     FOREIGN KEY (impacted_law)
     REFERENCES laws(law_num)
     )
    """
)
tables['users']=(
   "CREATE TABLE `users` ("
   "`username` varchar(30) NOT NULL,"
   "`email` varchar(20) NOT NULL,"
   "`password` varchar(15) NOT NULL,"
   "`first_name` varchar(15) NOT NULL,"
   "`last_name` varchar(15) NOT NULL,"
   "PRIMARY KEY(`username`)"
   ")ENGINE=InnoDB")

try:
    cnx = mc.connect(**config)
    cursor = cnx.cursor()

except mc.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print "Err: Access Denied (Verify user and password)"
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print "Database not found"
    else:
        print err
    sys.exit(1)

needed = dict(tables) # all tables need to be created
while needed:
    for name, cmd in tables.iteritems():
        if name in needed: # not already successfully created in loop
            try: #create table
        	print "Creating table {}:".format(name)
                cursor.execute(cmd)
                print "OK"
                del needed[name] #success
            except mc.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print "ALREADY EXISTS"
                    del needed[name]
                else:
                    print err.msg

cursor.close()
cnx.close()
