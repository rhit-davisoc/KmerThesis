import pandas as pd
import sys

input_folder = sys.argv[1]
output = sys.argv[2]

diff = 0
total = 0

with open(input_folder+"n0.fa") as file1:
    data1 = file1.read().replace('\n',' ')

with open(input_folder+"n1.fa") as file2:
    data2 = file2.read().replace('\n',' ')

for i in range(0,len(data1)):
    if data1[i] != data2[i]:
        diff += 1
    total += 1

file1.close()
file2.close()

diff -= 2

print("diff: %d,total: %d" %(diff,total))

f = open(output,"a")
f.write(str(diff))
f.close()