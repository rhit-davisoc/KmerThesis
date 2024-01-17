import pandas as pd
import sys

kmer_folder = sys.argv[1]
num_ind = int(sys.argv[2])
mut_rate = float(sys.argv[3])
coverage = int(sys.argv[4])
metric = sys.argv[5]
k = sys.argv[6]
output = sys.argv[7]

def CalcBCTwoIndividuals(file1,file2,inter_file):
    print("Calculating pair...")
    df1 = pd.read_csv(file1,sep="\t",header=None,names=["kmer","counts"])
    sum1 = sum(df1.counts)

    df2 = pd.read_csv(file2,sep="\t",header=None,names=["kmer","counts"])
    sum2 = sum(df2.counts)

    df_inter = pd.read_csv(inter_file,sep="\t",header=None,names=["kmer","counts"])
    sum_inter = sum(df_inter.counts)

    BC = 1 - (2*sum_inter/(sum1 + sum2))

    return BC

def update_write_file(score):
    print("Writing...")
    f = open(output,"a")
    f.write(metric + "," +str(mut_rate) + "," + str(coverage) + "," + str(k) + "," + str(score) + "\n")
    f.close()

pair = range(0,num_ind)

if(metric == "BC"):
    total_BC = 0
    total_pairs = 0
    for i in pair:
        for j in pair:
            if(i < j):
                file1 = kmer_folder + "n" + str(i) + ".txt"
                file2 = kmer_folder + "n" + str(j) + ".txt"
                inter_file = kmer_folder + "n" + str(i) + "_inter_n" + str(j) +  ".txt"
                total_BC += CalcBCTwoIndividuals(file1,file2,inter_file)
                total_pairs += 1

    BC = total_BC/total_pairs
    update_write_file(BC)

