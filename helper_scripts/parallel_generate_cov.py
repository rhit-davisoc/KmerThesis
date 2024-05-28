import os
import multiprocessing
from joblib import Parallel, delayed

num_cores = multiprocessing.cpu_count()
print("num_cpus: %d" % num_cores)

j = 40

test_path = "./arabidopsis_sim_data/"

coverages = [10,30]

start_id = 1507
end_id = 1808

def gen_coverage(id):
    for cov in coverages:
        sim_exists = os.path.isdir(test_path + "sim_" + str(id))
        if(sim_exists):
            print("./helper_scripts/generate_coverage.sh -d %d -c %d"%(id,cov))
            os.system("bash ./helper_scripts/generate_coverage.sh -d %d -c %d"%(id,cov))

processed_list = Parallel(n_jobs=j)(delayed(gen_coverage)(i) for i in range(start_id,end_id))