#!/bin/bash -l
#
#SBATCH --mail-user=sakre@ucdavis.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=resParse-1
#SBATCH --error=resParse-1.err
#SBATCH --partition=med
#SBATCH --account=millsgrp


#Run with: sbatch -p med -A millsgrp -t 36:00:00 --mem 1500 resParse.sh
module load biopython

python /home/sakre/projects/Res_BLAST/resParse.py test.htm final.contigs.fa DMDT001A 3 .9 /home/sakre/projects/Res_BLAST