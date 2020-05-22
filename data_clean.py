import numpy as np
import csv
def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])

def containsAny(string):
    chars = ['{', '}', '[', ']']
    for c in chars:
        if c in string: return 1
    return 0


newfile = open('5gram-edits-dev-sents-clean.csv','a+',newline='')
data = []
count_old = 0
count_edits = 0
count_sents = 0
with open('./5gram-edits-dev-sents-updated.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        #print(row)
        if len(row) <= 10:
            count_old += 1
            before = row[6]
            after = row[7]
            if len(before.split()) <= 5 and len(after.split()) <= 5:
                if levenshtein(before, after) >= 4:
                    if containsAny(before) == 0 and containsAny(after) == 0:
                        if len(before.split()) <= 1:
                            if before.lower() not in after.lower():
                                count_sents += 1
                                data.append(row)

with newfile:
    write = csv.writer(newfile)
    write.writerows(data)

print(count_old, count_edits, count_sents)
