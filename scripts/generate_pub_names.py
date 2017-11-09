# generate the names of the publications from the laws

from os import listdir
from os.path import isfile, join


onlyfiles = [f for f in listdir("demo_laws") if isfile(join("demo_laws", f))]

f = open("publication_names.txt", 'w')

for name in onlyfiles:
  #print name
  name = '/' + name
  ff = open("demo_laws"+name, 'r')
  pub_name = ff.read().split('\n')[3]
  f.write(pub_name + '\n')
  ff.close()

f.close() 
  
  


