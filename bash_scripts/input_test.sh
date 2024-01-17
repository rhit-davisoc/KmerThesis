# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
mut_rate=0.00001
coverage=0
num_indv=2
seed=101
div_metric="BC"
km=20

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -c|--cov) coverage="$2"; shift ;;
        -k|--kmer) km="$2"; shift ;;
        -m|--mut) mut_rate="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "coverage: $coverage and kmer: $km and mut: $mut_rate"