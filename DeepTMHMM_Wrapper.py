import argparse
import os
import re

from os import system

from Bio import SeqIO

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Print sequence IDs and lengths from a FASTA file.")
parser.add_argument(
    "-i", "--input",
    required=True,
    help="Input FASTA file"
)

args = parser.parse_args()

#Prepare fresh summary tsv
with open("DeepTMHMM-Summary.tsv", "w") as outfile2:
    print("Sequence ID", "Length", "No. TM Domains", sep="\t", file=outfile2)


# Read the FASTA file and get lengths of sequences
for record in SeqIO.parse(args.input, "fasta"):
    print(record.id, "\t", len(record.seq))

    #Write fasta to file
    with open("DeepTMHMM_Input.fasta", "w") as outfile1:
        print(">", record.id, record.seq, sep="\n", file=outfile1)

    #Run deeptmhmm
    os.system("python3 predict.py --fasta DeepTMHMM_Input.fasta --output-dir DeepTMHMM_Output_Directory")
    print("DeepTMHMM Complete for ", record.id)

    #Open deeptmhmm results
    with open("DeepTMHMM_Output_Directory/deeptmhmm_results.md", "r") as results:
        text = results.read()

    #Pull number of tms from results
    match = re.search("Number of predicted TMRs\:\s([0-7])", text)
    #print(match.group(0))  # Entire match
    #print(match.group(1))  # First capture group

    if match:
        number_of_tms = int(match.group(1)) #Get number of transmembrane domains
        print("Number of TMs: ",number_of_tms)

    #Write fasta to file
    with open("DeepTMHMM-Summary.tsv", "a") as outfile2:
        print(record.id, len(record.seq), number_of_tms, sep="\t", file=outfile2)

    #Delete deeptmhmm outputs to prepare for next sequence
    os.system("rm -r DeepTMHMM_Output_Directory/")
    os.system("rm DeepTMHMM_Input.fasta")