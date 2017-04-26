
 # Antibiotic Resistance Parser

 This script is intended to match potential antibiotic resistance found in WGS sample to the sequence in the WGS 
 data and run a blast search to determine what species it may have come from. Returns a CSV file of the data. Designed for use at the Mills Lab @ UC Davis.

## Usage: 
 python resParse.py [HTM_FILE] [CONTIG_FILE] [SAMPLE_ID] [NUMBER_OF_MATCHES] [IDENTITY_THRESHOLD] [OUT_DIR]

## Example: 
 python /home/sakre/projects/Res_BLAST/resParse.py test.htm final.contigs.fa DMDT001A 3 .9 /home/sakre/projects/Res_BLAST

 Example bash file to run script titled 'resParse.sh'

## Notes:
 Make sure to load biopython module, other dependencies are already loaded on the Farm
 Include full path to files needed
 Sample ID can be any string used to identify the input data
 Identity Threshold must be between 0 and 1
 
 Currently runs on the NCBI database so I do not suggest running too many of these in parallel in order to not overload their servers


Sincerely, <br>
Samir Akre <br>
[www.samirakre.com](http://www.samirakre.com)	
