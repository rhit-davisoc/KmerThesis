import os


test_path = "./arabidopsis_sim_data/"


start_id = 12
end_id = 1506
done = True

for i in range(start_id,end_id):
    print(i)
    src_read = "./arabidopsis_sim_data/sim_" + str(i) + "/reads"
    dest_read="./arabidopsis_sim_data/sim_" + str(i) + "/reads_x10"

    os.rename(src_read,dest_read)

    src_kmer = "./arabidopsis_sim_data/sim_" + str(i) + "/kmer_counts"
    dest_kmer="./arabidopsis_sim_data/sim_" + str(i) + "/kmer_counts_x10_k10"

    os.rename(src_kmer,dest_kmer)