# import content type

from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector

cnx = mysql.connector.connect(user='amucungu', password='m90753',
                              host='localhost',
                              database='rwandanlaw')

cursor = cnx.cursor()

add_content_type = ("INSERT INTO content_type "
                    "(name, authority) "
                    "VALUES (%s, %s)")

f = open("content_type.txt", "r")
contents = f.read().split('\n')

for cont_type in contents:
  if cont_type:
    cont_type = cont_type.split()
    cont_name, cont_autho = ' '.join(cont_type[1:]), cont_type[0]
    cont_tuple = (cont_name, cont_autho)
    cursor.execute(add_content_type, cont_tuple)
 
cnx.commit()
cursor.close()
cnx.close()


