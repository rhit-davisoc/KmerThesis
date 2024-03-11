import re

ref_seq = "./standard_test_data/fasta_files/standard_individual.fa"

with open(ref_seq) as file:
    data = file.read().replace('\n','').replace('>n0','')

data = re.sub(r'>n.',',',str(data))

file.close()