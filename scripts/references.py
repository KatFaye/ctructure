#coding: utf - 8
import os
import re
from fixlawname import FixLawName
articleNums=[]
for ref in os.listdir('demo_refs'):
  ref = 'demo_refs/' + ref
  previous_line=""
  i=0

  with open (ref) as reffile:

      for current_line in reffile:
          current_line = current_line.replace(",", "")
          current_line = current_line.replace(";", "")
          #print(current_line)

          if (i == 2):

              lawName = current_line
              print(lawName)
          elif(i==3):
              new_obj = FixLawName(current_line)
              copy = new_obj.copy_list()
              print(copy)

              for k in range(len(copy)):
                  for j in range(len(copy[k])-4):
                      token = copy[k][j]
                      if new_obj.is_law_name(copy, k, j):
                          if copy[k][j + 1][0].isdigit():
                              law_num = copy[k][j + 1]
                              law_date = copy[k][j + 3]
                              print(law_num, law_date)
              '''publicationDateMatch = re.findall(r'\d{2}/\d{2}/\d{4}', current_line)
              lawNumMatch = re.findall(r'\d{2}/\d{4}', current_line)
              if publicationDateMatch is not None:
                  articleNums = []
                  for s in current_line.split():
                    j=0
                    if s=="Articles":
                      articleNums.append(s)
                      j=j+1
                    #if s.isdigit():
                          #print(s)
                  print(publicationDateMatch)
              if lawNumMatch is not None:
                  print(lawNumMatch)'''
          i=i+1
          print("\n")