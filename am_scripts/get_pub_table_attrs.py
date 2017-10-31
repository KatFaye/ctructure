# Analyze the names of the publication names to extract the primary key
# Primary Key (var_num, pub_date)
# var_num can be official gazette "number", "number+bis", or "special"

filename = "publication_names.txt"

def get_pub_attrs(pub_name):
  # lenght should be above 3
  var_num, pub_date = '', ''
  pub_name = pub_name.split()
  if pub_name and len(pub_name) > 4:
    # 1. check if it has regular format
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
      print "Cannot find var_num in publication '{0}'".format(name)

    return var_num, pub_date


with open(filename, 'r') as f, open("pub_table_attributes.txt", "w") as ff:
  pub_dict = {} # store temporarily to remove duplicates
  pub_list = f.read().split('\n')
  for pub_name in pub_list:
    if pub_name:  
      var_num, pub_date = get_pub_attrs(pub_name)
      # Make sure it's "of" not "0f" [zero instead of o]
      pub_name_split = pub_name.split()
      for i in range(len(pub_name_split)):
        if pub_name_split[i].lower() == '0f': pub_name_split[i]='of'
  
      pub_name = ' '.join(pub_name_split)     
      # save to dictionary
      pub_dict[(var_num, pub_date)] = pub_name
  
  # write to file
  for item in pub_dict:
    ff.write(item[0]+' '+item[1] + ' '+pub_dict[item] + '\n')

