# import content agencies

from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector

cnx = mysql.connector.connect(user='amucungu', password='m90753',
                              host='localhost',
                              database='rwandanlaw')

cursor = cnx.cursor()

add_agency = ("INSERT INTO agencies "
                    "(abbrev, long_name) "
                    "VALUES (%s, %s)")

f = open("agencies.txt", "r")
contents = f.read().split('\n')

for agency in contents:
  if agency:
    agency = agency.split()
    abbrev, long_name = agency[0], ' '.join(agency[1:])
    cont_tuple = (abbrev, long_name)
    cursor.execute(add_agency, cont_tuple)
 
cnx.commit()
cursor.close()
cnx.close()


