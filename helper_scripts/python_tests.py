import random as rand
import os
from timeit import default_timer as timer
from joblib import Parallel, delayed

rand.seed(404)

test_path = "./arabidopsis_sim_data/"

muts = [0.000001,0.00001,0.00003,0.00005,0.0001,0.0002]
# muts = [0.00001]
coverages = [10]
ind = 10
j = 40

start_id = 1506
end_id = 2006

def create_sim(id):
    mut = muts[id%6]
    sim_exists = os.path.isdir(test_path + "sim_" + str(id))
    if(sim_exists != True):
        print("Making simulation %d...", id)
        os.system('bash ./helper_scripts/generate_standard_pop.sh -i %d -m %f -d %s' %(ind,mut,id))
    id += 1

processed_list = Parallel(n_jobs=j)(delayed(create_sim)(i) for i in range(start_id,end_id))