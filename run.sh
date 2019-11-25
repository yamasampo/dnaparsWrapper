#!/bin/bash

indir=$1
outdir=$2
jobs=$3

# Check command
# find $indir -type f -name "*.cod.aln" -maxdepth 1 | parallel -a - --dry-run ./bootstrap.sh

echo "INPUT: $indir"
echo "OUTPUT: $outdir"
echo "THREADNUM: $jobs"

mkdir ./output_dir
find "$indir" -type f -name "*.cod.fna.aln" -maxdepth 1 | parallel -a - --jobs "$jobs" ./bootstrap_dnapars.sh

mv ./output_dir "$outdir"

# Copy consensus trees
mkdir "$outdir"_tree
python copyNewickFiles.py "$outdir" "$outdir"_tree

# Reformat newick files
mkdir "$outdir"_tree_mod
python reformatPhylipNewick.py "$outdir"_tree "$outdir"_tree_mod
