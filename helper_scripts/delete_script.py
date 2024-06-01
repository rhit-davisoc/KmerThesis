import os
test_path = "./arabidopsis_sim_data/"

kmers=[10,20,30,40]
coverages = [10,30]

start_id = 1
end_id = 2006
done = True

for id in range(start_id,end_id):
    sim_exists = os.path.isdir(test_path + "sim_" + str(id))
    if(sim_exists == True):
        for cov in coverages:
            for kmer in kmers:
                sim_exists = os.path.isdir(test_path + "sim_" + str(id) + "/kmer_counts_x" + str(cov) + "_k" + str(kmer))
                if(sim_exists == True):
                    os.system('rm -r /home/davisoc/KmerThesis/arabidopsis_sim_data/sim_' + str(id) + "/kmer_counts_x" + str(cov) + "_k" + str(kmer))
                    print("Removed cov %d, kmer %d" % (cov,kmer))
        sim_exists = os.path.isdir(test_path + "sim_" + str(id) + "/reads_x" + str(cov))
        if(sim_exists == True):
            os.system('rm -r /home/davisoc/KmerThesis/arabidopsis_sim_data/sim_' + str(id) + '/reads_x' + str(cov))
    