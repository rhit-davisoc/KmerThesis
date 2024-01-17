from Bio import SeqIO
from random import sample
import os
import sys
import numpy as np

pop_fasta = sys.argv[1]

# pop_fasta = "./reads/true_div_rm_5/n0_R1.fastq"

sample_fasta = "sample_fasta.fa"

# sf = open(sample_fasta,"x")

# A[np.random.choice(A.shape[0], 2, replace=False), :]

for i in range(0,100000):
    os.system("./seqtk/seqtk sample -s11 ./reads/true_div_rm_5/n1_R2.fastq 1 >> test.fq")