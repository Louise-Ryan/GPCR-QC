# GPCR Classifier
Python wrapper implementing deeptmhmm to classify GPCR predictions based on the number of detected transmembrane domains.
Must be executed in the same directory where deeptmhmm is installed.

Takes only the amino acid fasta file as input:

```python3 Classify_GPCR.py -i <input_fasta.fa>```

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
