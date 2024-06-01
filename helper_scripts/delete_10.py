import os
test_path = "./arabidopsis_sim_data/"

start_id = 1
end_id = 2006
done = True

for id in range(start_id,end_id):
    sim_exists = os.path.isdir(test_path + "sim_" + str(id) + "/reads_x10")
    if(sim_exists == True):
        os.system('rm -r /home/davisoc/KmerThesis/arabidopsis_sim_data/sim_' + str(id) + '/reads_x10')
        print("Deleted x10 for sim " + str(id))
    