#!/bin/bash

## Commands to run dnapars with bootstrapped data

# Specify virtual environment for BioPython
source activate biopython

# Make output directory
input_fasta=$1
echo "$input_fasta"
outdir=./output_dir

# Make output directory
fname=`basename $input_fasta`
echo "$fname"
subdirname="$(cut -d'.' -f1 <<<"$fname")"
dirname="$outdir/$subdirname"
mkdir "$dirname"

# Convert FASTA to PhyLip format
python fasta2phylip.py "$input_fasta" "$dirname/infile_seqboot.phy"

# Bootstrap an alignment
cd "$dirname"
seqboot < ../../seqboot.ctl
# mv infile infile_seqboot
mv outfile outfile_seqboot

# Infer tree for bootstrap data
dnapars < ../../dnapars.ctl

mv outfile outfile_dnapars
mv outtree outtree_dnapars

# Find consensus tree
consense < ../../consense.ctl

mv outfile outfile_consense
mv outtree outtree_consense

cd ../
