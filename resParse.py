from bs4 import BeautifulSoup
import re
import sys
import subprocess
from Bio.Blast import NCBIWWW,NCBIXML
import csv

# This script is intended to match potential antibiotic resistance found in WGS sample to the sequence in the WGS 
# data and run a blast search to determine what species it may have come from. Returns a CSV file of the data.

#USAGE: 
# python resParse.py [HTM_FILE] [CONTIG_FILE] [SAMPLE_ID] [NUMBER_OF_MATCHES] [IDENTITY_THRESHOLD]

#EXAMPLE: 
# python /home/sakre/resParse.py test.htm final.contigs.fa DMDT001A 3 .9

#NOTES:
# Make sure to load biopython module, other dependencies are already loaded on the Farm
# Include full path to files needed
# Sample ID can be any string used to identify the input data
# Identity Threshold must be between 0 and 1
# Currently runs on the NCBI database so I do not suggest running too many of these in parallel in order to not overload their servers


HTM_FILE=sys.argv[1]
CONTIG_FILE=sys.argv[2]
SAMPLE_ID=sys.argv[3]
NUMBER_OF_MATCHES=int(sys.argv[4])
IDENTITY_THRESHOLD=int(sys.argv[5])

# Checking all inputs entered
if (HTM_FILE && CONTIG_FILE && SAMPLE_ID && NUMBER_OF_MATCHES && IDENTITY_THRESHOLD):
	print 'Running Script on Sample ID: '+SAMPLE_ID
else:
	print 'Error: Missing Values'
	print 'format: python resParse.py [HTM_FILE] [CONTIG_FILE] [SAMPLE_ID] [NUMBER_OF_MATCHES] [IDENTITY_THRESHOLD]'

#Adds Antiobiotic Resistance contigs to an array 'contigs'
print 'parsing htm file...'
with open(HTM_FILE,'r') as html_doc:
	soup = BeautifulSoup(html_doc, 'html.parser')

	results=[]
	tables=soup.find_all(class_="results")
	i=0
	for t in tables:
		tempTable=[]
		for row in t.find_all('tr'):
			tmp=row.find_all('td')
			if not tmp:
				tmp=row.find_all('th')

			tmp=[x.string for x in tmp]
			tempTable.append(tmp)
		results.append(tempTable)
		i=i+1
	data=[]
	for i in results:
		if len(i) !=2:
			data.append(i)

	contigs=[] #initializing results array
	for res in data:
		drug=res[0]
		for gene in res[2:]:
				#array format: Sample,Drug,Gene,Sequence Header
				contigs.append([SAMPLE_ID,str(drug[0]),str(gene[0]),str(gene[3])])
print 'done.'

#Reads data from contigs file to array 'data'
print'reading contig file..'
with open(CONTIG_FILE,'r') as file:
	data=file.readlines()
print'done'

#Adds contig sequences to contig array by searching for the header
print 'sorting contigs...'
for j,cont in enumerate(contigs):	
	pat=re.compile(cont[3])
	i=0
	for line in data:
		if(pat.search(line)):
			contigs[j].append(data[i]+data[i+1])
		i=i+1
print'done.'

#Writes results to a CSV File
k=0
with open(SAMPLE_ID+'_contig_blast.csv','wb') as csvfile:
	datawriter=csv.writer(csvfile)
	datawriter.writerow(['Sample','Resistance','Gene','Fasta Header']+['[Species,identity]']*NUMBER_OF_MATCHES)

	#Runs a blast search on each contig returning an array of format: [Sample,Drug,Gene,Sequence Header, [Species,identity]]
	for cont in contigs:
		print 'starting blast search number '+str(k)+' id: '+cont[3]+'...'
		fasta_string = cont[4]
		result_handle = NCBIWWW.qblast("blastn", "nt", fasta_string)
		contigs[k].pop() #removing sequence itself from result array
		print'done.'		

		print 'parsing result...'
		blast_record = NCBIXML.read(result_handle)
		

		matches=0

		for align in blast_record.alignments:
			if matches<NUMBER_OF_MATCHES:
				hsps=align.hsps
				identities=hsps[0].identities
				aLen=hsps[0].align_length
				identity=float(identities)/float(aLen)
				if identity>IDENTITY_THRESHOLD:
					matches=matches+1
					contigs[k].append([str(align.title),identity])
		print 'done.'

		print 'writing to csv file'
		datawriter.writerow(contigs[k])
		print 'done'
		k=k+1
		


