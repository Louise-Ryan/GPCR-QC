# 🧬 GPCR Quality Control (QC)
Python wrapper around DeepTMHMM for quality control and classification of predicted GPCR sequences based on the number of detected transmembrane domains. The pipeline automates DeepTMHMM execution, parses transmembrane domain predictions, and assigns sequences into complete GPCRs (7TM), partial predictions, putative fusions, or sequences lacking predicted transmembrane domains. 


---

## 📖 Contents

- [Installing DeepTMHMM](#installing-deeptmhmm)
- [Running the GPCR-QC Pipeline](#running-the-gpcr-qc-pipeline)
- [GPCR-QC Classification and Output Files](#gpcr-qc-classification-and-output-files)
- [Citation](#citation)

--- 

<a id ="installing-deeptmhmm"></a>
## 🛠️ Installing DeepTMHMM

**Licensing note:** Please refer to the official DeepTMHMM documentation for licensing details.

**Official instructions to install deepTMHMM locally can be found here:** 

https://dtu.biolib.com/DeepTMHMM/ 

**The following guide is also useful for troubleshooting installation:** 

https://www.polarmicrobes.org/local-installation-of-deeptmhmm/ 


**Configuring DeepTMHMM to be run from any directory (Optional):**

By default, this script should be run from the DeepTMHMM installation directory because it calls `predict.py` directly, which expects to find the required DeepTMHMM files in the current directory. To run the script from any location, you can create a wrapper script and add it to your system PATH, as described below:

1) Copy the following Bash script and save it as `deeptmhmm`. Before using it, update the `DEEPTMHMM` variable so that it points to your DeepTMHMM installation directory.

```bash
#!/bin/bash

DEEPTMHMM="/path/to/DeepTMHMM-Academic-License-v1.0"

# Remember the current working directory
WORKDIR=$(pwd)

# Change to the DeepTMHMM installation directory
cd "$DEEPTMHMM"

python predict.py \
    --fasta "$WORKDIR/$1" \
    --output-dir "$WORKDIR/$2"
```

2. Make the script executable:

```bash
chmod +x deeptmhmm
```

3. Move it to a directory in your `PATH` (for example, `/usr/local/bin` or `~/bin`):

```bash
mv deeptmhmm ~/bin/

or

sudo mv deeptmhmm /usr/local/bin/
```

Once the wrapper is available in your `PATH`, the `--system` option can be used to run the installed `deeptmhmm` command instead of the local `predict.py` script.

<br>

---

<a id="running-the-gpcr-qc-pipeline"></a>
## ⚙️ Running the GPCR-QC Pipeline

The pipeline requires a single input file: an amino acid FASTA file.

### Running from the DeepTMHMM installation directory (default)

By default, the pipeline executes `predict.py` directly. Therefore, it must be run from the DeepTMHMM installation directory.

```bash
python3 GPCR-QC.py -i <input_fasta.fa>
```

### Running from any directory (optional)

If you have configured the optional DeepTMHMM wrapper script and added it to your system `PATH`, you can use the `--system` (or `-s`) option to run the installed `deeptmhmm` command instead from any working directory.

```bash
python3 GPCR-QC.py -i <input_fasta.fa> --system
```

<br>

---

<a id="gpcr-qc-classification-and-output-files"></a>
## 📊 GPCR-QC Classification and Output files


### Classificationss:

<table>
  <tr align="left">
    <th>Number of TM Domains</th>
    <th>Classification</th>
    <th>Description</th>
  </tr>
  <tr align="left">
    <td>7</td>
    <td>Complete</td>
    <td>Complete GPCR prediction</td>
  </tr>
  <tr align="left">
    <td>0-7</td>
    <td>Partial</td>
    <td>Incomplete GPCR prediction</td>
  </tr>
  <tr align="left">
    <td>0</td>
    <td>No_TM_domains</td>
    <td>No predicted transmembrane domains</td>
  </tr>
  <tr align="left">
    <td>&gt;7</td>
    <td>Putative_fusion</td>
    <td>Potential fusion protein or multiple GPCR prediction</td>
  </tr>
</table>


### Output files:

<table>
  <tr>
    <th align="left">File</th>
    <th align="left">Description</th>
  </tr>
  <tr>
    <td align="left">Annotated_Sequences_Classified.fa</td>
    <td>FASTA file containing all input sequences with GPCR-QC classification and the number of DeepTMHMM-predicted transmembrane domains appended to each sequence header.</td>
  </tr>
  <tr>
    <td align="left">DeepTMHMM-Summary.tsv</td>
    <td>Tab-separated summary file containing sequence ID, sequence length, number of predicted transmembrane domains, and final GPCR-QC classification for each sequence.</td>
  </tr>
  <tr>
    <td align="left">Filtered_Sequences.fa</td>
    <td>FASTA file containing only sequences classified as complete GPCRs with exactly 7 predicted transmembrane domains, suitable for downstream analysis.</td>
  </tr>
</table>

<br>

---

<a id="citation"></a>
## 📄 Citation:

If you use this pipeline, please cite and provide a link to this GitHub repository: [Louise-Ryan/GPCR-QC](https://github.com/Louise-Ryan/GPCR-QC)

If you use **DeepTMHMM** as part of this wrapper, please cite the original authors:

> Hallgren J, Tsirigos KD, Pedersen MD, Armenteros JJA, Marcatili P, Nielsen H, Krogh A, Winther O. **DeepTMHMM predicts alpha and beta transmembrane proteins using deep neural networks.** *bioRxiv*. 2022. doi:10.1101/2022.04.08.487609.
 
 
