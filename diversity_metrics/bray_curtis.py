import pandas as pd
import sys
import numpy as np
import mmh3
from sklearn.metrics.pairwise import cosine_similarity


kmer_folder = sys.argv[1]
num_ind = int(sys.argv[2])
mut_rate = float(sys.argv[3])
coverage = int(sys.argv[4])
metric = sys.argv[5]
k = sys.argv[6]
output = sys.argv[7]

def CalcBCTwoIndividuals(df1,df2,inter_file):
    print("Calculating pair...")
    # df1 = pd.read_csv(file1,sep="\t",header=None,names=["kmer","counts"])
    sum1 = sum(df1.counts)

    # df2 = pd.read_csv(file2,sep="\t",header=None,names=["kmer","counts"])
    sum2 = sum(df2.counts)

    df_inter = pd.read_csv(inter_file,sep="\t",header=None,names=["kmer","counts"])
    sum_inter = sum(df_inter.counts)

    BC = 1 - (2*sum_inter/(sum1 + sum2))

    return BC

def CalcBFTwoIndividuals(df1,df2,h):
    print("Calculating pair...")

    num_hash = h
    total = df1.shape[0]
    array_size = 8*400000

    array1 = np.zeros(array_size,dtype=np.int16)
    array2 = np.zeros(array_size,dtype=np.int16)

    # df1 = pd.read_csv(file1,sep="\t",header=None,names=["kmer","counts"])
    kmers1 = df1.kmer
    counts1 = df1.counts
    total = df1.shape[0]

    for i in range(0,total):
        for k in range(0, num_hash):
            index = mmh3.hash(kmers1[i],k,signed=False)%array_size
            array1[index] += counts1[i]

    # df2 = pd.read_csv(file2,sep="\t",header=None,names=["kmer","counts"])
    kmers2 = df2.kmer
    counts2 = df2.counts
    total = df2.shape[0]

    for i in range(0,total):
        for k in range(0, num_hash):
            index = mmh3.hash(kmers2[i],k,signed=False)%array_size
            array2[index] += counts2[i]
            # array1[index] -=  counts2[i]

    # cosine = np.dot(array1,array2)/(np.linalg.norm(array1)*np.linalg.norm(array2))
    # array1mag = np.sqrt(np.sum(array1**2))
    # array2mag = np.sqrt(np.sum(array2**2))

    # top = np.sum(array1*array2)
    # bottom = (array1mag*array2mag)

    # print("numbers:")
    # print(top)
    # print(bottom)

    # cosine = np.sum(array1)/(array1mag*array2mag)
    # cosine = distance.cosine(array1,array2)
    cosine = cosine_similarity([array1],[array2])

    return cosine[0][0]

def update_write_file(score,m,td,h):
    print("Writing...")
    f = open(output,"a")
    f.write(td + "," + m + "," +str(mut_rate) + "," + str(coverage) + "," + str(k) + "," + str(score) + "," + str(h) + "\n")
    f.close()

pair = range(0,num_ind)


true_div = 0
with open("./true_div/div.txt") as f:
    true_div = f.readline()

total_measure1 = 0
total_measure2 = 0
total_measure3 = 0
total_measure4 = 0
total_pairs = 0

hashes = [5,6,7]

for i in pair:
    for j in pair:
        if(i < j):
            file1 = kmer_folder + "n" + str(i) + ".txt"
            df1 = pd.read_csv(file1,sep="\t",header=None,names=["kmer","counts"])
            file2 = kmer_folder + "n" + str(j) + ".txt"
            df2 = pd.read_csv(file2,sep="\t",header=None,names=["kmer","counts"])
            inter_file = kmer_folder + "n" + str(i) + "_inter_n" + str(j) +  ".txt"

            total_measure1 += CalcBCTwoIndividuals(df1,df2,inter_file)
            total_measure2 += CalcBFTwoIndividuals(df1,df2,5)
            total_measure3 += CalcBFTwoIndividuals(df1,df2,6)
            total_measure4 += CalcBFTwoIndividuals(df1,df2,7)
            total_pairs += 1

            score = total_measure1/total_pairs
            update_write_file(score,"BC",true_div,0)

            score = total_measure2/total_pairs
            update_write_file(score,"BF",true_div,5)

            score = total_measure3/total_pairs
            update_write_file(score,"BF",true_div,6)

            score = total_measure4/total_pairs
            update_write_file(score,"BF",true_div,7)

