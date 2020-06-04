import numpy as np
import csv
import re
data = []
newfile_strongsubj = open('strongsubj.csv','a+',newline='')
newfile_weaksubj = open('weaksubj.csv','a+',newline='')

headers = ['Subjectivity Type','Length of Sentence','Word','Stemmed','Priorpolarity']

with open('./subjclueslen1.txt', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        row_data = []
        for elem in row[0].split():
            res = re.sub(r'.*\=',"",elem)
            row_data.append(res)
        data.append(row_data)

strongsubj = []
weaksubj = []
for row in data:
    if row[0] == 'strongsubj':
        strongsubj.append([row[2],row[-1]])
    elif row[0] == 'weaksubj':
        weaksubj.append([row[2],row[-1]])
print(strongsubj)

with newfile_strongsubj:
    write = csv.writer(newfile_strongsubj)
    write.writerows(strongsubj)
with newfile_weaksubj:
    write = csv.writer(newfile_weaksubj)
    write.writerows(strongsubj)
