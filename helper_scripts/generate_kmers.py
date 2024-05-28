import os
import multiprocessing
from joblib import Parallel, delayed

num_cores = multiprocessing.cpu_count()
print("num_cpus: %d" % num_cores)

j = 40

test_path = "./arabidopsis_sim_data/"

kmers=[10,20,30,40]
coverages = [10,30]

start_id = 1507
end_id = 1808
done = True

def gen_kmers(id):
# for id in range(start_id,end_id):
    for kmer in kmers:
        for cov in coverages:
            sim_exists = os.path.isdir(test_path + "sim_" + str(id) + "/kmer_counts_x" + str(cov) + "_k" + str(kmer))
            if(sim_exists == False):
                os.chdir('/home/davisoc/KmerThesis/arabidopsis_sim_data/sim_' + str(id))
                print("generating k: %d, id: %i, c: %d,"%(kmer,id,cov))
                os.system('bash ../../helper_scripts/subsample.sh -k %d -d %d -c %d' %(kmer,id,cov))
                os.chdir('/home/davisoc/KmerThesis/')

processed_list = Parallel(n_jobs=j)(delayed(gen_kmers)(i) for i in range(start_id,end_id))

# for id in range(start_id,end_id):
#     for kmer in kmers:
#         for cov in coverages:
#             for ind in indvs:
#                 # os.system('bash helper_scripts/subsample.sh -k %d -d %d -c %d' %(kmer,id,cov))
#                 print("hi k: %d, id: %i, c: %d,"%(kmer,id,cov))