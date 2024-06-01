import sys
import os

start = 22
end = 301

for i in range(start,end):
    print("i: %d" % i)
    os.system("gzip -r -v ./arabidopsis_sim_data/sim_%d/reads_x10" % i)
    os.system("gzip -r -v ./arabidopsis_sim_data/sim_%d/reads_x30" % i)
    os.mkdir("./sim_data_gzip/sim_%d" % i)
    os.system("cp -r ./arabidopsis_sim_data/sim_%d/reads_x10 ./sim_data_gzip/sim_%d" % (i,i))
    os.system("cp -r ./arabidopsis_sim_data/sim_%d/reads_x30 ./sim_data_gzip/sim_%d" % (i,i))