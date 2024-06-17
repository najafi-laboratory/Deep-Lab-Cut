#!/bin/bash
#SBATCH -JDLC-FN16			# Job Name
#SBATCH --account=gts-fnajafi3		# Charge Account
#SBATCH -N1 --gres=gpu:V100:1     		# Number of nodes and cores per node required
#SBATCH --gres-flags=enforce-binding
#SBATCH --mem-per-gpu=12G               # Memory per core
#SBATCH -t2880                           # Duration of the job (Ex: 300 mins)
#SBATCH -oReport-%j.out                         # Combined output and error messages file
#SBATCH --mail-type=BEGIN,END,FAIL              # Mail preferences
#SBATCH --mail-user=ydhadwal3@gatech.edu        # E-mail address for notifications

source /storage/home/hcoda1/3/ydhadwal3/myenv/bin/activate

cd /storage/coda1/p-fnajafi3/0/ydhadwal3/FN13_Joystick_0603-Yuvraj-2024-06-17             # Change to working directory

module load cuda/12.1.1-6oacj6

#pip install deeplabcut
#pip install ipython
#pip install --upgrade tensorflow==2.12.0

/storage/home/hcoda1/3/ydhadwal3/myenv/bin/python main.py


