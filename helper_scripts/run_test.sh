# Run a full test that generates a population with the following variables and calculates the diversity of the sampled individuals
# Written by Olivia Davis

OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
# Model Variables
mut_rate=0.00001
coverage=10
num_indv=2
seed=101
div_metric="BC"
km=10
cpus=50
min_count=5
test_name="bc_hashes"
type="BC"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -c|--cov) coverage="$2"; shift ;;
        -k|--kmer) km="$2"; shift ;;
        -m|--mut) mut_rate="$2"; shift ;;
        -n|--name) test_name="$2"; shift ;;
        -t|--type) type="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "coverage: $coverage and kmer: $km and mut: $mut_rate"


# File / Naming Variables
# test_name="true_div_rm_5"
tree_file_name=$test_name".trees"
tree_path="./SLIM/generated_trees/"$tree_file_name
output_file="./output/"$test_name".csv"

# Helper Variables (don't change)
reads=$(echo $((coverage*2033342/126)))
#158730
fasta_file_name=$test_name".fa"
fasta_file_path="./fasta_files/"$fasta_file_name
split_fasta_path="./fasta_files/"$test_name"/"
read_file_path="./reads/"$test_name"/"

# [Commands Run]


# Simulate population with SLIM. Add mutations and sample n individuals from population to create multi fasta file. (where n = num_indv)

./SLIM/slimexe -d "file_name='./SLIM/generated_trees/$tree_file_name'" -d mut_rate=$mut_rate ./SLIM/generate_tree.slim &&

python3 ./tskit_msprime/tree_to_fasta.py $tree_path $fasta_file_path $seed $num_indv&&

mkdir $split_fasta_path &&

python3 ./tskit_msprime/splitfasta.py $fasta_file_path $split_fasta_path &&

python3 ./tskit_msprime/count_snps.py $split_fasta_path ./true_div/div.txt
# Simulate reads from fasta files

mkdir $read_file_path &&

for i in $(seq 0 $((num_indv-1)))
do
    iss generate --genomes $split_fasta_path"n"$i".fa" --cpus $cpus --n_reads $reads --model hiseq --output $read_file_path"/n"$i
done


# Get kmer counts with KMC3

mkdir ./kmer_counts/tmp/
mkdir ./kmer_counts/tmp/$test_name"/" &&
mkdir ./kmer_counts/$test_name"/" &&

for i in $(seq 0 $((num_indv-1)))
do
    KMC3/kmc -t$cpus -k$km -ci$min_count $read_file_path"n"$i"_R1.fastq" ./kmer_counts/tmp/$test_name"/n"$i"_R1" .&&

    KMC3/kmc -t$cpus -k$km -ci$min_count $read_file_path"n"$i"_R2.fastq" ./kmer_counts/tmp/$test_name"/n"$i"_R2" . &&

    ./KMC3/bin/kmc_tools -t$cpus simple ./kmer_counts/tmp/$test_name"/n"$i"_R1" ./kmer_counts/tmp/$test_name"/n"$i"_R2" union ./kmer_counts/tmp/$test_name/n$i &&

    ./KMC3/bin/kmc_tools -t$cpus transform ./kmer_counts/tmp/$test_name/n$i  dump ./kmer_counts/$test_name/n$i.txt
done

for i in $(seq 0 $((num_indv-1)))
do
    for j in $(seq 0 $((num_indv-1)))
    do
        if [ $i -lt $j ]
        then
            ./KMC3/bin/kmc_tools -t$cpus simple ./kmer_counts/tmp/$test_name"/n"$i ./kmer_counts/tmp/$test_name"/n"$j intersect ./kmer_counts/tmp/$test_name/n$i"_n"$j &&

            ./KMC3/bin/kmc_tools -t$cpus transform ./kmer_counts/tmp/$test_name/n$i"_n"$j  dump ./kmer_counts/$test_name/n$i"_inter_n$j".txt
        fi
    done
done

# Calculate diversity score

python ./diversity_metrics/bray_curtis.py ./kmer_counts/$test_name"/" $num_indv $mut_rate $coverage $div_metric $km $output_file