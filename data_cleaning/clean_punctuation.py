import numpy as np
import csv
data = ['Before Edit','After Edit','Before Edit Sentence','After Edit Sentence']
newfile = open('train-sents-final.csv','a+',newline='')

with open('./5gram-edits-train-sents-clean.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        before = row[6].replace('.','').replace(',','').lower()
        after = row[7].replace('.','').replace(',','').lower()
        sents_before = row[8].replace('.','').replace(',','').lower()
        sents_after = row[9].replace('.','').replace(',','').lower()
        before = before.replace('.','').replace(',','').lower()
        data.append([before,after,sents_before,sents_after])

with newfile:
    write = csv.writer(newfile)
    write.writerows(data)
