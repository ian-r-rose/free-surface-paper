#!/bin/bash
#
# name of this script: program-batch.sh
#
# Job name:
#SBATCH --job-name=nsfd
#
# Partition:
#SBATCH --partition=BB
#
# Processors:
#SBATCH --ntasks=32
#SBATCH --ntasks-per-core=1
#SBATCH --ntasks-per-node=8
#SBATCH -vv
#
# Mail type:
#SBATCH --mail-type=all
#
# Mail user:
#SBATCH --mail-user=ian.r.rose@gmail.com
#
#cmd="mpirun /home/ian.rose/aspect/build/aspect crameri_benchmark_2.prm"
cmd="python run_models.py"
echo $cmd
$cmd
