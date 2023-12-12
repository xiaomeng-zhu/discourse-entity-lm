#!/bin/sh

#SBATCH --job-name=my_job_gpu
#SBATCH --time=12:00:00
#SBATCH --mail-type=ALL
#SBATCH --partition gpu
#SBATCH --gpus=a100:1

module load miniconda
conda activate /gpfs/gibbs/project/frank/ref4/conda_envs/py38-condgen-2/
python llama/llama-gpu.py