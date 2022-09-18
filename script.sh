#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --mem-per-cpu=1G
#SBATCH --time=0-04:00
module load anaconda3
conda init bash
conda activate getafix_honours
python3 rapiscript_rep_first_3.py






