# import_all_data.py
# insert data into tables of the Rwandanlaw database
# Group: Ctructure
# Date: 10/30/2017


from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
from os import listdir
from os.path import isfile, join

# folders and files with the raw data
folder_of_laws = "demo_laws/"
folder_of_intros = "demo_refs/"
file_of_agencies = "agencies.txt"
file_of_content_types = "content_types.txt"

# list of individual files within a directory
law_files = [f for f in listdir(folder_of_laws) if isfile(join(folder_of_laws, f))]
intro_files = [f for f in listdir(folder_of_intros) if isfile(join(folder_of_laws, f))]

# create connection to the database
cnx = mysql.connector.connect(user='amucungu', password='m90753',
                              host='0.0.0.0',
                              database='rwandanlaw')

cursor = cnx.cursor()

### Defined functions
def get_pub_attrs(pub_name):
  # lenght should be above 3
  var_num, pub_date = '', ''
  pub_name = pub_name.split()
  if pub_name and len(pub_name) > 4:
    # check if it has regular format
    if pub_name[3].isdigit() and pub_name[4].lower() in ['of', '0f']:
      var_num = pub_name[3]
    # 2. Check if it has "bis"
    if pub_name[3].isdigit() and pub_name[4].lower() == 'bis':
      var_num = pub_name[3] + '_bis'
    # . Check if it is "special"
    if len(pub_name) > 3 and pub_name[3].lower() == 'special':
      var_num = 'special'

    pub_date = pub_name[-1] # date is the last thing 
    if var_num == '' or pub_date == '': # if either is still an empty string
      name = ' '.join(pub_name)
      #print "Cannot find var_num in publication "+"'"+name+"'"
    return var_num, pub_date
    
### IMPORT DATA for the "content_type" TABLE
add_content_type = ("INSERT INTO content_type "
                    "(name, authority) "
                    "VALUES (%s, %s)")

with open(file_of_content_types, "r") as f:
  contents = f.read().split('\n')

for cont_type in contents:
  if cont_type:
    cont_type = cont_type.split()
    cont_name, cont_autho = ' '.join(cont_type[1:]), cont_type[0]
    cont_tuple = (cont_name, cont_autho)
    cursor.execute(add_content_type, cont_tuple)

### IMPORT DATA for the "agencies" TABLE
add_agency = ("INSERT INTO agencies "
                    "(abbrev, long_name) "
                    "VALUES (%s, %s)")

with open(file_of_agencies, "r") as f:
  contents = f.read().split('\n')

for agency in contents:
  if agency:
    agency = agency.split()
    abbrev, long_name = agency[0], ' '.join(agency[1:])
    cont_tuple = (abbrev, long_name)
    cursor.execute(add_agency, cont_tuple)

### IMPORT DATA for the "publications" TABLE

add_publication = ("INSERT INTO publications "
                    "(var_num, name, pub_date) "
                    "VALUES (%s, %s, %s)")

# list of all publication names encountered in law files
publication_names = []

# get publication names for law files
for filename in law_files:
  with open(folder_of_laws +filename, 'r') as f:
    pub_name = f.read().split('\n')[3]
    publication_names.append(pub_name)

# dictionary of unique publications in law files
unique_publications = {}


# Extract publication table attributes from publication names
for publication in publication_names:
    if publication:
      #print(publication)
      var_num, pub_date = get_pub_attrs(publication)
      # Make sure it's "of" not "0f" [zero instead of o]
      split_pub = publication.split()
      for i in range(len(split_pub)):
        if split_pub[i].lower() == '0f': split_pub[i]='of'
      publication = ' '.join(split_pub)
      # save to the dictionary
      # key = (var_num, pub_date) is unique for each publication
      error_msg = "Cannot find var_num and pub_date for '{0}'" 
      assert var_num != '' and pub_date != '', error_msg.format(publication)
      unique_publications[(var_num, pub_date)] = publication

# Insert attributes into the "publications" table
for pub in unique_publications:
    # var_num & pub_date are part of the key, at index 0 and 1
    var_num, pub_date, name = pub[0], pub[1],' '.join(pub[2:])
    day, month, year = [int(i) for i in pub_date.split('/')]

    cont_tuple = (var_num, name, date(year, month, day))
    cursor.execute(add_publication, cont_tuple)

### COMMIT THE ABOVE THE DATA TO THE DATABASE
cnx.commit()
### Foreign key constraints the "laws" table requires to commit
### Before we try to insert data into the table

### IMPORT DATA for the "repeal" TABLE
add_repeal = ("INSERT INTO repeals"
                    "(parent_law_num, parent_law_date, impacted_law_num, impacted_law_date) "
                    "VALUES (%s, %s, %s, %s)")

repeal_list = []
with open('import_data/repeals.txt') as f:
    for line in f:
        line = line.rstrip()
        temp_list = line.split(",")
        repeal_list.append(temp_list)

# Insert attributes into the "repeal" table
for a_law in repeal_list:
    # var_num & pub_date are part of the key, at index 0 and 1
    parent_law_num, parent_law_date = a_law[0], a_law[1]
    p_day, p_month, p_year = [int(i) for i in parent_law_date.split('/')]
    impacted_law_num, impacted_law_date = a_law[2], a_law[3]
    i_day, i_month, i_year = [int(i) for i in impacted_law_date.split('/')]
    
    cont_tuple = (parent_law_num, date(p_year, p_month, p_day), impacted_law_num, date(i_year, i_month, i_day))
    cursor.execute(add_repeal, cont_tuple)
### COMMIT THE ABOVE THE DATA TO THE DATABASE
cnx.commit()

###IMPORT DATA into the "cites" TABLE
add_cites = ("INSERT INTO cites"
                    "(parent_law_num, parent_law_date, cited_law_num, cited_law_date) "
                    "VALUES (%s, %s, %s, %s)")

cite_list = []
with open('import_data/references.txt') as f:
    for line in f:
        if str(line).split():
            line = line.rstrip()
            temp_list = line.split(", ")
            cite_list.append(temp_list)

# Insert attributes into the "cites" table
for a_law in cite_list:
    if a_law:
        # var_num & pub_date are part of the key, at index 0 and 1
        parent_law_num, parent_law_date = a_law[0], a_law[1]
        p_day, p_month, p_year = [int(i) for i in parent_law_date.split('/')]
        cited_law_num, cited_law_date = a_law[2], a_law[3]
        c_day, c_month, c_year = [int(i) for i in cited_law_date.split('/')]

    cont_tuple = (parent_law_num, date(p_year, p_month, p_day), cited_law_num, date(c_year, c_month, c_day))
    cursor.execute(add_cites, cont_tuple)
### COMMIT THE ABOVE THE DATA TO THE DATABASE
cnx.commit()


### IMPORT DATA into the "laws" TABLE
add_law = ("INSERT INTO laws "
           "(law_num, exact_date, name, ending, pub_id, intro, content_type) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s)")

for law in law_files:
  # open law file and file with references
  with open(folder_of_laws + law, 'r') as f, \
  open(folder_of_intros + law + "_referencedLaws", 'r') as ff:

    # Querry pub ID
    q_pub_id = ("SELECT pub_id FROM publications "
                "WHERE var_num LIKE %s AND pub_date like %s")

    # Format of law_files is consistent. 
    # Indices below correspond to specific lines.
    law_doc = f.read().split('\n')
    intro = ff.read().split('\n')[3]
    content_type = law_doc[1] 
    law_name = law_doc[2] 
    law_num = law_name.split()[1]
    publication = law_doc[3]
    # get publication attributes
    pub_var_num, pub_date = get_pub_attrs(publication)
    ending = "N/A" # place_holder for now
    agency = "RRA"   # placeholder for now
    print(law_name)
    # exact date i.e. the date in the law's name or "exact_date" attribute
    e_day, e_month, e_year = [int(j) for j in law_name.split()[3].split('/')]
    # publication date i.e. "pub_date" attribute
    p_day, p_month, p_year = [int(i) for i in pub_date.split('/')]

    # Execute the q_law_id and q_pub_id queries
    q_law_content = (law_num, date(e_year, e_month, e_day))
    q_pub_content = (pub_var_num, date(p_year, p_month, p_day))
    cursor.execute(q_pub_id, q_pub_content)

    # get the result of the query above. 
    # fetchall() returns list of tuples (each tuple is a result)
    pub_id = cursor.fetchall()[0][0]
    cont_tuple = (law_num, date(e_year, e_month, e_day), law_name, \
                  ending, pub_id, intro, content_type)

    # insert into the "laws" table
    cursor.execute(add_law, cont_tuple)

### commit since the "articles" TABLE below references the "laws" Table
cnx.commit()

### IMPORT DATA into the "articles" TABLE
### We could add articles at the same time as laws 
### THOUGH, this allows to modify each table separately
add_article = ("INSERT INTO articles "
               "(law_id, article_num, article_text, name) "
               "VALUES (%s, %s, %s, %s)")

# we insert articles for each law at a time
for law in law_files:
  # open law file and file with references
  with open(folder_of_laws + law, 'r') as f:
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
    # articles start at index 6 (= line 7) in the law files
    for i in range(6, len_law_file, 2):
      if law_doc[i]:
        line_i = law_doc[i].split() # splitting the line i NOT i + 1
        article_num = line_i[1] # article is at index 1 in the line
        article_name = ' '.join(line_i[2:])
        article_text = law_doc[i+1]

        cont_tuple = (law_id, article_num, article_text, article_name)
        cursor.execute(add_article, cont_tuple)

# commit last changes and close connections
cnx.commit()
cursor.close()
cnx.close()

#print "Successfully imported all the data!"
