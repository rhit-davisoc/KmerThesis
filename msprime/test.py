import msprime
import pyslim
from IPython.display import SVG, display

# Simulate an ancestral history for 3 diploid samples under the coalescent
# with recombination on a 5kb region with human-like parameters.
ts = msprime.sim_ancestry(
    samples=3,
    recombination_rate=1e-8,
    sequence_length=5_000,
    population_size=10_000,
    random_seed=123456)

mts = msprime.sim_mutations(ts, rate=0.001, random_seed=5678)

# nts = pyslim.generate_nucleotides(mts)
# nts = pyslim.convert_alleles(nts)

print(f"The tree sequence now has {mts.num_mutations} mutations,\n"
      f"and mean pairwise nucleotide diversity is {mts.diversity():0.3e}.")

mts.write_fasta("test3.fasta")