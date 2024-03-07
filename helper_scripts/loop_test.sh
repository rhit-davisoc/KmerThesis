for i in {0..2}
do
    bash ./bash_scripts/clean.sh
    bash ./bash_scripts/run_test.sh -c 20 -k 30 -m 0
done

for i in {0..2}
do
    bash ./bash_scripts/clean.sh
    bash ./bash_scripts/run_test.sh -c 30 -k 10 -m 0
done

for i in {0..2}
do
    bash ./bash_scripts/clean.sh
    bash ./bash_scripts/run_test.sh -c 30 -k 20 -m 0
done

for i in {0..2}
do
    bash ./bash_scripts/clean.sh
    bash ./bash_scripts/run_test.sh -c 30 -k 30 -m 0
done