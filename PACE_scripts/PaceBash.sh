#!/bin/bash
#SBATCH -JDLC-FN14-20240710			# Job Name
#SBATCH --account=gts-fnajafi3		# Charge Account
#SBATCH -N1 --gres=gpu:V100:1     		# Number of nodes and cores per node required
#SBATCH --gres-flags=enforce-binding
#SBATCH --mem-per-gpu=12G               # Memory per core
#SBATCH -t2880                          # Duration of the job (Ex: 2880 mins or 2 days)
#SBATCH -oReport-%j.out                         # Combined output and error messages file
#SBATCH --mail-type=BEGIN,END,FAIL              # Mail preferences
#SBATCH --mail-user=ydhadwal3@gatech.edu        # E-mail address for notifications

cd /storage/coda1/p-fnajafi3/0/ydhadwal3/20240710-Yuvraj_Dhadwal-2024-07-24     # Change to working directory

module load anaconda3
conda activate DEEPLABCUT

LD_LIBRARY_PATH=/storage/home/hcoda1/3/ydhadwal3/.conda/envs/DEEPLABCUT/lib:$LD_LIBRARY_PATH python main.py