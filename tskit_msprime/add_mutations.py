import msprime
import tskit
import pyslim
import numpy as np

# Read in tree simulated from SLIM

orig_ts = tskit.load("./SLIM/simulated_ts.trees")


# Recapitate tree
rts = pyslim.recapitate(orig_ts,
            recombination_rate=1e-8,
            ancestral_Ne=200, random_seed=5)

# Simply tree down to a specified number of individuals.
rng = np.random.default_rng(seed=3)
alive_inds = pyslim.individuals_alive_at(rts, 0)
keep_indivs = rng.choice(alive_inds, 100, replace=False)
keep_nodes = []
for i in keep_indivs:
  keep_nodes.extend(rts.individual(i).nodes)

sts = rts.simplify(keep_nodes, keep_input_roots=True)


# Add mutations to tree with given rate, mu.
mts = msprime.sim_mutations(sts, rate=1e-9, random_seed=5678)

print(f"The tree sequence now has {mts.num_mutations} mutations,\n"
      f"and mean pairwise nucleotide diversity is {mts.diversity():0.3e}.")

mts.write_fasta("./fasta_files/simulated_fasta.fa")