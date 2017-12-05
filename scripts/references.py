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
              new_obj = FixLawName(current_line)
              copy = new_obj.copy_list()
              #print(copy)

              for k in range(len(copy)):
                  for j in range(len(copy[k]) - 4):
                      token = copy[k][j]
                      if new_obj.is_law_name(copy, k, j):
                          if copy[k][j + 1][0].isdigit():
                              parent_law_num = copy[k][j + 1]
                              parent_law_date = copy[k][j + 3]

          elif(i==3):
              new_obj = FixLawName(current_line)
              copy = new_obj.copy_list()
              #print(copy)

              for k in range(len(copy)):
                  for j in range(len(copy[k])-4):
                      token = copy[k][j]
                      if new_obj.is_law_name(copy, k, j):
                          if copy[k][j + 1][0].isdigit():
                              law_num = copy[k][j + 1]
                              law_date = copy[k][j + 3]
                              #print("parent law:")
                              print(parent_law_num+",",parent_law_date+",",law_num+",",law_date)
                              #print("references:")
                              #print(law_num, law_date)


          i=i+1
