import mysql.connector as mc
import cgi


config = {
    'user': 'kherring',
    'password': '12faye',
    'host': '127.0.0.1',
    'database': 'rwandanlaw'
}

form=cgi.FieldStorage()

data = {
 'law_search_bar': form.getvalue('law_search_bar')
 'date_bar': form.getvalue('date_bar')
}

sql= "SELECT name FROM laws l, publications p inner join l.pub_id=p.pub_id "
         "WHERE name like '%s%' and month(p.pub_date)=%s")%(data['law_search_bar'],data['date_bar'])

try:
    cnx = mc.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(sql)

print(name)

cursor.close()
cnx.close()

