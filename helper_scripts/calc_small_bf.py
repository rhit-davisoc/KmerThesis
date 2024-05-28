import random as rand
import os
import pandas as pd
from timeit import default_timer as timer
from joblib import Parallel, delayed

rand.seed(404)

test_path = "./arabidopsis_sim_data/"

kmers=[10,20,30,40]
coverages = [10,30]
indv = 10
j = 20
remove_k = 5

start_id = 13
end_id = 300
done = True

def get_num_ind(id):
    info_path = test_path + "sim_" + str(id) + "/sim_info_" + str(id) + ".csv"
    info = pd.read_csv(info_path)
    ind = info.iloc[0,4]
    return ind

def calc_scores(id):
    # print(os.getcwd())
    sim_path = test_path + "sim_" + str(id) + "/"
    sim_exists = os.path.isdir(sim_path)
    if(sim_exists == True):
        print("Calculating simulation %d scores..." % id)
        for kmer in kmers:
            for cov in coverages:
                kmer_folder = sim_path + "kmer_counts_x" + str(cov) + "_k" + str(kmer) + "/P0/"
                # kmer_folder = sim_path
                kmers_exists = os.path.isdir(kmer_folder)
                if(kmers_exists):
                    ind = get_num_ind(id)
                    output = sim_path + "sim_" + str(id) + "_results_rm5.csv"
                    csv_exists = os.path.isfile(output)
                    if(csv_exists == False):
                        print("Creating file...")
                        file = open(output, 'w')
                        file.write("id,coverage,k-length,metric,score\n")
                        file.close()
                    cmd = "python ./diversity_metrics/BF_small_array.py {} {} {} {} {} {}".format(id,kmer,cov,ind,kmer_folder,output)
                    os.system(cmd)
                else:
                    print("Kmer does not exists:")
                    print(kmer_folder)
    else:
        print("Directory does not exist:")
        print(sim_path)

processed_list = Parallel(n_jobs=j)(delayed(calc_scores)(i) for i in range(start_id,end_id))