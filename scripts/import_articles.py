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

add_article = ("INSERT INTO articles "
               "(law_id, article_num, article_text, name) "
               "VALUES (%s, %s, %s, %s)")

onlyfiles = [f for f in listdir("demo_laws") if isfile(join("demo_laws", f))]

for law in onlyfiles:
  # open law file and file with references
  with open("demo_laws/"+law, 'r') as f:
    law_doc = f.read().split('\n')
    law_name = law_doc[2].split()
    law_num = law_name[1]
    exact_date = law_name[3]
    day, month, year = [int(i) for i in exact_date.split('/')]
    exact_date = date(year, month, day)   

    # Querry law_ID 
    q_law_id = ("SELECT law_id FROM laws "
               "WHERE law_num LIKE %s AND exact_date LIKE %s ")
    q_content = (law_num, exact_date)
    cursor.execute(q_law_id, q_content)
    law_id = cursor.fetchall()[0][0]
   
    len_law_file = len(law_doc)
    # articles start at index 6
    for i in range(6, len_law_file, 2):
      if law_doc[i]:
        line_i = law_doc[i].split() # splitting the line i NOT i + 1
        article_num = line_i[1] # article is at index 1 in the line
        article_name = ' '.join(line_i[2:])
        article_text = law_doc[i+1]

        cont_tuple = (law_id, article_num, article_text, article_name)
        cursor.execute(add_article, cont_tuple)

cnx.commit()
cursor.close()
cnx.close()

  
