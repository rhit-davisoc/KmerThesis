import pandas as pd
import sys

kmer_folder = sys.argv[1]
num_samples = int(sys.argv[2])
mut_rate = float(sys.argv[3])
coverage = int(sys.argv[4])
metric = sys.argv[5]
k = sys.argv[6]
output = sys.argv[7]
sample_folder = sys.argv[8]
id = sys.argv[9]

def CalcBCTwoIndividuals(file1,sum2,inter_file):
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
    f.write(str(id) + "," + metric + "," +str(mut_rate) + "," + str(coverage) + "," + str(k) + "," + str(score) + "\n")
    f.close()

samps = range(0,num_samples)

if(metric == "BC"):
    total_BC = 0
    total_pairs = 0

    file2 = kmer_folder + "n1.txt"
    df2 = pd.read_csv(file2,sep="\t",header=None,names=["kmer","counts"])
    sum2 = sum(df2.counts)

    for i in samps:
        file1 = sample_folder + "n" + str(i) + ".txt"
        inter_file = sample_folder + "samp_n" + str(i) + "_union_n1.txt"
        BC = CalcBCTwoIndividuals(file1,sum2,inter_file)
        update_write_file(BC)

