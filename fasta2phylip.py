#!/usr/bin/python3

import sys
from Bio import AlignIO

def convert(fasta_path, out_path):
    with open(fasta_path, 'r') as f:
        with open(out_path, 'w') as out:
            alignments = AlignIO.parse(f, 'fasta')
            AlignIO.write(alignments, out, 'phylip')


if __name__ == '__main__':
    fasta_path = sys.argv[1]
    out_path = sys.argv[2]
    convert(fasta_path, out_path)
    