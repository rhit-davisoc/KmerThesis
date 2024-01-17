import random as rand
import os

rand.seed(404)

mut_low = 0
muts = [0.00001,0.000001]

coverages = [10,20,30,40]
kmer_sizes = [10,20,30,40]

NUM_LOOPS = 10

for i in range(0,NUM_LOOPS):
    for mut in muts:
        for cov in coverages:
            for kmer in kmer_sizes:
                os.system('bash ./bash_scripts/clean.sh')
                os.system('bash ./bash_scripts/run_test.sh -c %d -k %d -m %f' %(cov,kmer,mut))