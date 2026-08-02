# GPCR Quality Control (QC)
Simple python wrapper implementing deepTMHMM to classify GPCR predictions based on the number of detected transmembrane domains.
Must be executed in the same directory where deepTMHMM is installed.

Official instructions to install deepTMHMM locally can be found:
https://dtu.biolib.com/DeepTMHMM/ 

The following guide is also useful for troubleshooting installation:
https://www.polarmicrobes.org/local-installation-of-deeptmhmm/ 

Takes only the amino acid fasta file as input:

```python3 GPCR-QC.py -i <input_fasta.fa>```

<br>

<b>Classifications are as follows:</b>
- 7 TM domains: Complete
- \> 0, < 7 TM domains: Partial
- 0 TM domains: No_TM_domains
- \> 7 TM domains: Putative_fusion

<br>

<b>Output files:</b>
- Annotated_Sequences_Classified.fa # Fasta file containing input sequences with classification in sequence header
- DeepTMHMM-Summary.tsv # Sumamry TSV file with sequence ID, length, No. TM domains and Classification
- Filtered_Sequences.fa # Filtered/clean fasta file containing only sequences with 7 TM domains

<br>

<b>Citation</b>

If you use **DeepTMHMM** as part of this wrapper, please cite the original authors:

> Hallgren J, Tsirigos KD, Pedersen MD, Armenteros JJA, Marcatili P, Nielsen H, Krogh A, Winther O. **DeepTMHMM predicts alpha and beta transmembrane proteins using deep neural networks.** *bioRxiv*. 2022. doi:10.1101/2022.04.08.487609.
 
 
