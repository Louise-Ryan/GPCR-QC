import argparse
import subprocess
import re
from Bio import SeqIO
import random
import string

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Print sequence IDs and lengths from a FASTA file.")
parser.add_argument( "-i", "--input", required=True, help="Input FASTA file")
parser.add_argument( "-s", "--system", action="store_true", help="Use the system-installed 'deeptmhmm' command instead of the local predict.py script.")
args = parser.parse_args()

#Prepare fresh summary tsv
summary_tsv_out = open("DeepTMHMM-Summary.tsv", "w")
print(
    "Sequence ID",
    "Length",
    "No. TM Domains",
    "Classification",
    sep="\t",
    file=summary_tsv_out
)

#Initiate Fresh output file for classified sequences
annotated_seqs_out = open("Annotated_Sequences_Classified.fa", "w")

#Initiate fresh file to print filtered sequences
filtered_seqs_out = open("Filtered_Sequences.fa","w")

#Check that sequenceIDs are unique
new_file = None
sequences = list(SeqIO.parse(args.input, "fasta"))

# Check that sequence IDs are unique
sequence_ids = [seq.id for seq in sequences]
if len(sequence_ids) != len(set(sequence_ids)):
    print(f"Sequence IDs are not unique, there are {len(sequence_ids)} sequences but {len(set(sequence_ids))} unique headers")
    new_file = args.input + "_unique_identifiers.fa"
    print(f"Adding unique identifiers and writing to {new_file}")
    used_ids = set()  # store new IDs

    for seq in sequences:
        old_id = seq.id
        old_description = seq.description
        while True:
            new_id = "SeqID_" + ''.join(random.choices(string.digits, k=6))
            if new_id not in used_ids:
                used_ids.add(new_id)
                break
        seq.id = new_id + "_" + old_id
        seq.description = seq.id + old_description[len(old_id):]
        
    # Write updated sequences once
    with open(new_file, "w") as unique_id_out:
        SeqIO.write(sequences, unique_id_out, "fasta")

else:
    print("Sequence IDs are unique, proceed")

#Specify whether to use unique_ID file or orginal file name   
if new_file:
    input_file = new_file
else:
    input_file = args.input


#Run deeptmmm
if args.system:
    subprocess.run(
        [
            "deeptmhmm",
            input_file,
            "DeepTMHMM_Output_Directory"
        ],
        check=True
    )
else:
    subprocess.run(
        [
            "python3",
            "predict.py",
            "--fasta", input_file,
            "--output-dir", "DeepTMHMM_Output_Directory"
        ],
        check=True
    )


#Parse deeptmhmm results
deeptmhmm_results = {}

#Open deeptmhmm results
with open("DeepTMHMM_Output_Directory/TMRs.gff3", "r") as results:
    for line in results:
        tm_match = re.search(r"#\s(\S+)\sNumber\sof\spredicted\sTMRs:\s(\d+)", line)  
        if tm_match:
            seqid = tm_match.group(1)
            number_of_tms = int(tm_match.group(2))
            deeptmhmm_results[seqid] = number_of_tms

#Loop through sequences and write to outputfiles
for seq in sequences:
    number_of_tms = deeptmhmm_results.get(seq.id)
    if number_of_tms is None:
        number_of_tms = "NA"
        print(f"Couldn't determine TM domains for {seq.id}")
    
    classification = ""
    #If deepTMHMM fails, then NA
    if number_of_tms == "NA":
        classification = "NA"

    #If TM = 7, Complete prediction 
    elif number_of_tms == 7:
        classification = "Complete"

        #Print complete sequences to filtered file
        print(">", seq.description,
                " [classification=", classification,
                "] [DeepTMHMM Domains=", number_of_tms, "]",
                sep="",
                file=filtered_seqs_out
            )
        seq_string = str(seq.seq)
        for i in range(0, len(seq_string), 80):
                print(seq_string[i:i + 80], file=filtered_seqs_out)

    #Classify incomplete, partial or fusion predictions
    elif number_of_tms > 0 and number_of_tms < 7:
        classification = "Partial"
    elif number_of_tms > 7:
        classification = "Putative_fusion"
    elif number_of_tms == 0:
        classification = "No_TM_domains"

    #Write summary to file
    print(seq.description, 
          len(seq.seq), 
          number_of_tms, 
          classification, 
          sep="\t", 
          file=summary_tsv_out)

    #Classify OR in sequence file
    print(
        ">", seq.description,
        " [classification=", classification,
        "] [DeepTMHMM Domains=", number_of_tms, "]",
        sep="",
        file=annotated_seqs_out
    )
    seq_string = str(seq.seq)
    for i in range(0, len(seq_string), 80):
        print(seq_string[i:i + 80], file=annotated_seqs_out)


filtered_seqs_out.close()
summary_tsv_out.close()
annotated_seqs_out.close()
