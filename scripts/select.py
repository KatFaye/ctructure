import mysql.connector as mc


config = {
    'user': 'kherring',
    'password': '12faye',
    'host': '127.0.0.1',
    'database': 'rwandanlaw'
}
cnx = mc.connect(**config)
cursor = cnx.cursor()

query = ("SELECT law_num FROM laws "
         "WHERE law_id<50")


cursor.execute(query)

for (law_num) in cursor:
  print("law_num is {}").format(law_num)

cursor.close()
cnx.close()
