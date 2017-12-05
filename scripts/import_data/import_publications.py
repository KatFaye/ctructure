# import publications

from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector

cnx = mysql.connector.connect(user='amucungu', password='m90753',
                              host='localhost',
                              database='rwandanlaw')

cursor = cnx.cursor()

add_publication = ("INSERT INTO publications "
                    "(var_num, name, pub_date) "
                    "VALUES (%s, %s, %s)")

f = open("pub_table_attributes.txt", "r")
contents = f.read().split('\n')

for pub in contents:
  if pub: # if the item is not empty
    pub = pub.split()
    # 1st element is var_num, 2nd is date, the rest is name
    var_num, pub_date, name = pub[0], pub[1],' '.join(pub[2:])
    day, month, year = [int(i) for i in pub_date.split('/')]
   
    cont_tuple = (var_num, name, date(year, month, day))
    cursor.execute(add_publication, cont_tuple)
 
cnx.commit()
cursor.close()
cnx.close()


