#coding: utf - 8
import os
import re
lawNameArray=[]
publicationDateArray=[]
lawNumArray=[]
articleNumArray=[]
for law in os.listdir('demo_laws'):
  law = 'demo_laws/' + law
  previous_line=""
  i=0
  with open (law) as lawfile:
    for current_line in lawfile:
        current_line=current_line.replace(",", "")
        if(i==2):
            lawName=current_line
            #print(lawName)
            currentLawName=current_line
        wordArray=previous_line.split(" ")
        if(len(wordArray)>2):
            if(wordArray[2]=="repealing"):
                print(current_line)
                publicationDateMatch = re.search(r'\d{2}/\d{2}/\d{4}', current_line)
                lawNumMatch=re.search(r'\d{2}/\d{4}',current_line)
                if publicationDateMatch is not None:
                    articleNums=[]
                    for s in current_line.split():
                        if s.isdigit():
                            articleNums.append(s)
                    articleNumArray.append(articleNums)
                    lawNametoStore=lawName
                    lawNameArray.append(lawName)
                    publicationDate=publicationDateMatch.group()
                    publicationDateArray.append(publicationDate)
                    print(publicationDateMatch.group())
                    print(lawNametoStore)
                if lawNumMatch is not None:
                    lawNum=lawNumMatch.group()
                    lawNumArray.append(lawNum)
                    print(lawNumMatch.group())
        previous_line=current_line
        i=i+1
print(articleNumArray)









