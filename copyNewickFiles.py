#!/usr/bin/python3

import sys
import os
import fnmatch

def copy_tree_files(
    in_dir, out_dir, 
    in_file_pat='outtree_consense', 
    out_suffix='.dnapars.consense.newick.txt'):
    for fpath in gen_find_file(in_dir, in_file_pat):
        name = os.path.basename(os.path.dirname(fpath))
        to_fpath = os.path.join(out_dir, f'{name}{out_suffix}')
        
        with open(fpath, 'r') as f:
            oneline = ''.join([l.rstrip() for l in f])
            
        with open(to_fpath, 'w') as out:
            print(oneline, file=out)
        
    return to_filelist(out_dir)

def gen_find_file(top, filepat):
    """ Find all filenames in a directory tree that match a shell wildcard 
    pattern. """
    for path, _, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)

def to_filelist(dir_path):
    """ Return a list of file names of a given directory and save as 
    "0.filelist" in the directory. 
    """
    flist= [
        fname for fname in os.listdir(dir_path) 
            if not fname.startswith('.') and not fname.startswith('0')
    ]

    with open(os.path.join(dir_path, '0.filelist'), 'w') as f:
        print('itemnum: '+str(len(flist)), file=f)
        print('\n'.join(flist), file=f)
    return flist

if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    flist = copy_tree_files(in_dir, out_dir)
    print(f'{len(flist)} files saved in {out_dir}.\n')
