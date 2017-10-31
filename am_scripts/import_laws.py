## Import demo laws into mysql


from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
from os import listdir
from os.path import isfile, join

from get_pub_table_attrs import get_pub_attrs # locally defined function

cnx = mysql.connector.connect(user='amucungu', password='m90753',
                              host='localhost',
                              database='rwandanlaw')

cursor = cnx.cursor()

add_law = ("INSERT INTO laws "
           "(law_num, exact_date, name, ending, pub_id, intro, content_type, agency) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

onlyfiles = [f for f in listdir("demo_laws") if isfile(join("demo_laws", f))]

for law in onlyfiles:
  # open law file and file with references
  with open("demo_laws/"+law, 'r') as f, open("demo_refs/"+law+"_referencedLaws", 'r') as ff:
    
    # Querry pub ID
    q_pub_id = ("SELECT pub_id FROM publications "
                "WHERE var_num LIKE %s AND pub_date like %s")

    law_doc = f.read().split('\n')
    intro = ff.read().split('\n')[3] # ref at line 4

    content_type = law_doc[1] # type of "law"
    law_name = law_doc[2] # name of "law"
    law_num = law_name.split()[1]
    # exact date i.e. the date in the law's name
    e_day, e_month, e_year = [int(j) for j in law_name.split()[3].split('/')]
    ending = "N/A"
    agency = law_doc[4]
    publication = law_doc[3]
    # get attributes for a publication
    pub_var_num, pub_date = get_pub_attrs(publication)
    # publication date i.e. p_date
    p_day, p_month, p_year = [int(i) for i in pub_date.split('/')]
    agency = "RRA"   # placeholder for now
    
    # Execute q_pub_id queries
    q_pub_content = (pub_var_num, date(p_year, p_month, p_day))
    cursor.execute(q_pub_id, q_pub_content)
    
    # after calling fetchall(), the cursor object becomes empty
    pub_id = cursor.fetchall()[0][0] # only one element
    cont_tuple = (law_num, date(e_year, e_month, e_day), law_name, \
                  ending, pub_id, intro, content_type, agency)
    cursor.execute(add_law, cont_tuple)

cnx.commit()
cursor.close()
cnx.close()

  
