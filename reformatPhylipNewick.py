#!/usr/bin/python3

import os
import re
import sys

def reformat_newicks(
    in_dir, out_dir, 
    pat_list=[r':\d+\.\d+[,\)]', r'\)[,\)]']):
    flist = read_filelist(os.path.join(in_dir, '0.filelist'))
    
    error_items = []
    for fname in flist:
        tree_path = os.path.join(in_dir, fname)
        out_path = os.path.join(out_dir, fname[:-4]+'.mod.txt')
        
        try:
            newick = reformat_newick(tree_path, pat_list)
        except:
            error_items.append(fname)
            continue
        
        with open(out_path, 'w') as f:
            print(newick, file=f)
            
    return to_filelist(out_dir), error_items

def reformat_newick(newick_path, pat_list):
    def func(newick, pat):
        # Get bootstrap values
        # If bootstrap value is following to terminal edge, value is not stored.
        matches = list(re.finditer(pat, newick))
        
        if len(matches) == 0:
            return newick
        
        bootvs = []
        for m in matches:
            if newick[m.start()-1]==')':
                bootvs.append(m.group()[1:-1]+':')
            elif m.group(0).startswith(')'):
                bootvs.append(')0.0:')
            else:
                if float(m.group()[1:-1]) != 1000:
                    raise ValueError(f'Wrong Bootstrap value {m.group()[1:-1]} in {newick_path}.')
                bootvs.append('')

        # Replace bootstrap values with the combined items
        parts = []
        end = 0
        for m, item  in zip(matches, bootvs):
            parts += [
                newick[end:m.start()],
                item
            ]
            end = m.end()-1

        if m.end() < len(newick):
            parts += [newick[end:]]

        out_newick = ''.join(parts)
        check_parenthesis(out_newick)
        check_semicolon(out_newick)

        return out_newick

    newick = get_newick_str(newick_path)
    for pat in pat_list:
        newick = func(newick, pat)
        
    return newick
    
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

def read_filelist(filelist_path):
    with open(filelist_path, 'r') as f:
        return [line.rstrip() for line in f if not line.startswith('itemnum')]

def check_parenthesis(tree):
    opencnt, closecnt = tree.count('('), tree.count(')')
    assert opencnt == closecnt, f'Number of parenthesis are different. {opencnt} != {closecnt}.'
    
def check_semicolon(tree):
    assert tree.endswith(';'), f'Given tree does not end with ";", {tree}.'

def get_newick_str(tree_path):
    lines = []
    with open(tree_path, 'r') as f:
        for line in f:
            lines.append(line.rstrip())
            
    tree = ''.join(lines)
    check_parenthesis(tree)
    check_semicolon(tree)
    
    return tree

def remove_bootstrap_and_blength_values(tree):
    # Replace bootstrap values with the combined items
    parts = []
    end = 0
    for i, m in enumerate(re.finditer(r':\d+\.\d+[,\)]', tree)):
        parts.append(tree[end:m.start()])
        end = m.end()-1

    if m.end() < len(tree):
        parts.append(tree[end:])

    return ''.join(parts)
    
if __name__ == '__main__':
    in_dir, out_dir = sys.argv[1], sys.argv[2]
    flist, error_list = reformat_newicks(in_dir, out_dir)
    print(f'{len(flist)} files saved in {out_dir} and {len(error_list)} errors found.\n')
