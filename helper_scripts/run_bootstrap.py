import random as rand
import os

rand.seed(404)

test_name="bootstrap_k20_c20"

mut_low = 0
muts = [0.000001]

coverages = [20]
kmer_sizes = [20]

NUM_LOOPS = 1
index = 0

for i in range(0,NUM_LOOPS):
    for mut in muts:
        for cov in coverages:
            for kmer in kmer_sizes:
                os.system('bash ./helper_scripts/clean.sh')
                os.system('bash ./helper_scripts/run_test.sh -c %d -k %d -m %f -n %s' %(cov,kmer,mut,test_name))
                os.system('bash ./helper_scripts/bootstrap_test.sh -c %d -k %d -m %f -n %s -i %d' %(cov,kmer,mut,test_name,index))
                index+=1