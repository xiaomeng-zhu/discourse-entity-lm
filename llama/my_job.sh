#!/bin/sh

#SBATCH --job-name=my_job
#SBATCH --time=1-12:00:00
#SBATCH --mail-type=ALL
#SBATCH --partition week
#SBATCH --mem=32G

module load miniconda
conda activate /gpfs/gibbs/project/frank/ref4/conda_envs/py38-condgen-2/
python llama/llama.py