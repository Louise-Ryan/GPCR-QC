import argparse
import os
import re
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

#Initiate Fresh output file for classified sequences
open("Annotated_Sequences_Classified.fa", "w").close()

#Open file to print filtered sequences
filtered_seqs = open("Filtered_Sequences.fa","w")

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
    match = re.search("Number of predicted TMRs\:\s([0-9]+)", text)

    #Print failed sequence to screen
    if not match:
        print(f"Couldn't determine TM domains for {record.id}")
        number_of_tms = "NA"

    else:
        #Get number of TM domains and classify
        number_of_tms = int(match.group(1)) #Get number of transmembrane domains
        print("Number of TMs: ",number_of_tms)

    classification = ""
    #If deepTMHMM fails, then NA
    if number_of_tms == "NA":
        classification = "NA"

    #If TM = 7, Complete prediction 
    elif number_of_tms == 7:
        classification = "Complete"

        #Print complete sequences to filtered file
        print(">", record.description,
                " [classification=", classification,
                "] [DeepTMHMM Domains=", number_of_tms, "]",
                sep="",
                file=filtered_seqs
            )
        seq = str(record.seq)
        for i in range(0, len(seq), 80):
                print(seq[i:i + 80], file=filtered_seqs)

    #Classify incomplete, partial or fusion predictions
    elif number_of_tms > 0 and number_of_tms < 7:
        classification = "Partial"
    elif number_of_tms > 7:
        classification = "Putative_fusion"
    elif number_of_tms == 0:
        classification = "No_TM_domains"


    #Write summary to file
    with open("DeepTMHMM-Summary.tsv", "a") as outfile2:
        print(record.description, len(record.seq), number_of_tms, classification, sep="\t", file=outfile2)

    #Classify OR in sequence file
    # Write summary to file
    with open("Annotated_Sequences_Classified.fa", "a") as outfile3:
        print(
            ">", record.description,
            " [classification=", classification,
            "] [DeepTMHMM Domains=", number_of_tms, "]",
            sep="",
            file=outfile3
        )
        seq = str(record.seq)
        for i in range(0, len(seq), 80):
            print(seq[i:i + 80], file=outfile3)

    #Delete deeptmhmm outputs to prepare for next sequence
    os.system("rm -r DeepTMHMM_Output_Directory/")
    os.system("rm DeepTMHMM_Input.fasta")

filtered_seqs.close()