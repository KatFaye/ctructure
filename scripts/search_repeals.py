#coding: utf - 8

import re
lawNameArray=[]
publicationDateArray=[]
lawNumArray=[]
articleNumArray=[]
parentPublicationDateArray=[]
parentLawNumArray=[]
previous_line=""
i=0
with open('repeals_mod.txt') as lawfile:
    for current_line in lawfile:
        current_line = current_line.replace(",", "")
        if (current_line == "\n"):
            i = -1
        elif (i == 0):
            lawName = current_line
            parentPublicationDateMatch = re.search(r'\d{2}/\d{2}/\d{4}', current_line)
            parentLawNumMatch = re.search(r'\d{2}/\d{4}', current_line)
            if parentPublicationDateMatch is not None:
               parentPublicationDate= parentPublicationDateMatch.group()
               parentPublicationDateArray.append(parentPublicationDate)
            if parentLawNumMatch is not None:
                parentLawNum = parentLawNumMatch.group()
                parentLawNumArray.append(parentLawNum)
            #print(lawName)
            #currentLawName = current_line

        elif (i == 1):
            #print(current_line)
            publicationDateMatch = re.search(r'\d{2}/\d{2}/\d{4}', current_line)
            lawNumMatch = re.search(r'\d{2}/\d{4}', current_line)
            if publicationDateMatch is not None:
                articleNums = []
                for s in current_line.split():
                    if s.isdigit():
                        articleNums.append(s)
                articleNumArray.append(articleNums)
                #lawNametoStore = lawName
                lawNameArray.append(lawName)
                publicationDate = publicationDateMatch.group()
                publicationDateArray.append(publicationDate)

                #print(lawNametoStore)
            if lawNumMatch is not None:
                lawNum = lawNumMatch.group()
                lawNumArray.append(lawNum)
                print(parentLawNum)
                print(parentPublicationDate)

                print(lawNumMatch.group())
                print(publicationDateMatch.group())
                print("\n")
        previous_line = current_line
        i = i + 1
    print(articleNumArray)












