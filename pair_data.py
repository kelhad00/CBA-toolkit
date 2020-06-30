import sys
import argparse
from IBPY.db import *
from os import listdir

def check_dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def parse_arguments():
    parser = argparse.ArgumentParser(prog='Print pairs.')
    parser.add_argument('--path_ccdb', type=check_dir_path, help='Path to the CCDB annotation directory.')
    parser.add_argument('--path_ifadv', type=check_dir_path, help='Path to the IFADV annotation directory.')
    parser.add_argument('--path_ndc', type=check_dir_path, help='Path to the NDC-ME annotation directory.')
    args = parser.parse_args()
    return args, parser

def main():
    args, parser = parse_arguments()
    if not len(sys.argv) > 1:
        parser.print_help()
    if args.path_ccdb:
        lst = listdir(args.path_ccdb)
        pairs = form_pairs_ccdb(lst) # extract pairs for CCDB
        for p1, p2 in pairs:
            print('{} paired with {}'.format(p1, p2))
    if args.path_ifadv:
        lst = listdir(args.path_ifadv)
        pairs = form_pairs_ifadv(lst) # extract pairs for IFADV
        for p1, p2 in pairs:
            print('{} paired with {}'.format(p1, p2))
    if args.path_ndc:
        lst = listdir(args.path_ndc)
        pairs = form_pairs_ndc(lst) # extract pairs for NDC
        for p1, p2 in pairs:
            print('{} paired with {}'.format(p1, p2))

if __name__ == '__main__':
    main()
