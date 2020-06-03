import numpy as np
import csv
data = []
newfile = open('dev-sents-final1.csv','a+',newline='')

def containsAny(string):
    chars = ['{', '}', '[', ']','|','*']
    for c in chars:
        if c in string: return 1
    return 0

with open('./5gram-edits-dev-sents-clean.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        before = row[6].replace('.','').replace(',','').replace('"','').lower()
        after = row[7].replace('.','').replace(',','').replace('"','').lower()
        sents_before = row[8].replace('.','').replace(',','').replace('"','').lower()
        sents_after = row[9].replace('.','').replace(',','').replace('"','').lower()
        if containsAny(sents_before) == 0:
            if sents_before != sents_after:
                data.append([before,after,sents_before,sents_after])


with newfile:
    write = csv.writer(newfile)
    write.writerows(data)
