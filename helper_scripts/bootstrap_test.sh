mut_rate=0.00001
coverage=10
num_samples=1
seed=101
div_metric="BC"
km=10
cpus=50
min_count=5
test_name="test"
index=0

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -c|--cov) coverage="$2"; shift ;;
        -k|--kmer) km="$2"; shift ;;
        -m|--mut) mut_rate="$2"; shift ;;
        -n|--name) test_name="$2"; shift ;;
        -i|--id) index="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# File / Naming Variables
# test_name="true_div_rm_5"
tree_file_name=$test_name".trees"
tree_path="./SLIM/generated_trees/"$tree_file_name
output_file="./output/"$test_name"_samples.csv"

# Helper Variables (don't change)
reads=$(echo $((coverage*2033342/126)))
sample_reads=1
#158730
fasta_file_name=$test_name".fa"
fasta_file_path="./fasta_files/"$fasta_file_name
split_fasta_path="./fasta_files/"$test_name"/"
read_file_path="./reads/"$test_name"/"
sample_file_path="./read_samples/"$test_name"/"

mkdir ./kmer_counts/samples/&&
mkdir ./kmer_counts/samples/tmp/&&
mkdir ./kmer_counts/samples/tmp/$test_name"/" &&
mkdir ./kmer_counts/samples/$test_name"/" &&
mkdir ./read_samples/$test_name"/" &&

python helper_scripts/randomReadSubSample.py -f1 reads/$test_name/n0_R1.fastq -f2 reads/$test_name/n0_R2.fastq -s $sample_reads -r 1 -n $num_samples -o read_samples/$test_name/n0

for i in $(seq 0 $((num_samples-1)))
do
    KMC3/kmc -t$cpus -k$km -ci$min_count $sample_file_path"n0_"$i".1.fq" ./kmer_counts/samples/tmp/$test_name"/samp_n"$i"_R1" .&&

    KMC3/kmc -t$cpus -k$km -ci$min_count $sample_file_path"n0_"$i".2.fq" ./kmer_counts/samples/tmp/$test_name"/samp_n"$i"_R2" . &&

    ./KMC3/bin/kmc_tools -t$cpus simple ./kmer_counts/samples/tmp/$test_name"/samp_n"$i"_R1" ./kmer_counts/samples/tmp/$test_name"/samp_n"$i"_R2" union ./kmer_counts/tmp/$test_name/samp_n$i &&

    ./KMC3/bin/kmc_tools -t$cpus transform ./kmer_counts/tmp/$test_name/samp_n$i  dump ./kmer_counts/samples/$test_name/n$i.txt
done

for i in $(seq 0 $((num_samples-1)))
do
    ./KMC3/bin/kmc_tools -t$cpus simple ./kmer_counts/tmp/$test_name/samp_n$i ./kmer_counts/tmp/$test_name"/n1" intersect ./kmer_counts/samples/tmp/$test_name/samp_n$i"_union_n1" &&

    ./KMC3/bin/kmc_tools -t$cpus transform ./kmer_counts/samples/tmp/$test_name/samp_n$i"_union_n1" dump ./kmer_counts/samples/$test_name/samp_n$i"_union_n1.txt"
done

# Calculate diversity score

python ./diversity_metrics/bc_bootstrap.py ./kmer_counts/$test_name"/" $num_samples $mut_rate $coverage $div_metric $km $output_file ./kmer_counts/samples/$test_name"/" $index