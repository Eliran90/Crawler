import csv

file1 = open('count_word_per_page_20_pages_query_1.csv', "r") #Open CSV File in Read Mode
reader1 = csv.reader(file1)      #Create reader object which iterates over lines


class Object:                   # Object to store unique data
    def __init__(self, name, count):
        self.name = name
        self.count = int(count)


rownum = 0  # Row Number currently iterating over
list = []  # List to store objects
list2 = []  # List to store names
list3 = []  # List to store objects


def checkList(name):
    counter = 0
    flag = 0
    for object in list:  #Iterate through list
        if name in list3:
            flag = 1
            break
        if object.name == name:
            counter += int(object.count)
    if flag == 0:
        newObject = Object(name, counter)
        list2.append(newObject)  #Add to list and break out
        list3.append(name)  #Add to list and break out


for row in reader1:  #Iterate through all the rows
        name = row[0]  #Store name
        count = row[1]  #Store count
        newObject = Object(name, count)
        list.append(newObject)

file1.seek(0)

for row in reader1:  #Iterate through all the rows
        name = row[0]  #Store name
        count = row[1]  # Store count
        checkList(name)


CSV = open('top15_20pages.csv', 'w+', encoding='utf-8')
fieldnames = ['word', 'count']
writer1 = csv.DictWriter(CSV, fieldnames=fieldnames)
list4 = []  #List to store objects
newlist = []
for each in list2: #Print out result
    list4.append(dict(word=each.name, count=each.count))

for i in range(len(list4)):
    writer1.writerow(list4[i])

file1.close() #Close file