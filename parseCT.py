import argparse
import os
from typing import List

from ctparser import ClinicalTrialsParser


parser = argparse.ArgumentParser(prog="parseCT.py",
                                usage='%(prog)s [options] path',
                                description='Download/parse ClinicalTrials.gov XML files')

# Add the arguments
parser.add_argument('-i',
                       '--input',
                       type=str,
                       default='kinase_data/kinase_inhibitors.txt',
                       help='path to file with target medications')

# Execute the parse_args() method
args = parser.parse_args()

input_path = args.input


def get_kinase_list(path: str) -> List:
    """
    The expected input to this script is a file with the name of one medication per line.
    For instance, 
    
    afatinib
    imatinib
    (...)

    This function extracts a list of unique entries
    """
    if not os.path.exists(path):
        raise FileNotFoundError("Could not find %s." % path)
    protein_kinase_inhibitors = []
    with open(path) as f:
        for line in f:
            if len(line) > 1:
                protein_kinase_inhibitors.append(line.rstrip())
    protein_kinase_inhibitors = list(dict.fromkeys(protein_kinase_inhibitors))
    print(protein_kinase_inhibitors)
    return protein_kinase_inhibitors




def main():
    ctp = ClinicalTrialsParser()
    protein_kinase_inhibitors = get_kinase_list(args.input)
    fh = open('clinical_trials_pki_studies.tsv', 'wt')
    fh.write("%s\n" % ctp.get_header())
    for pki in protein_kinase_inhibitors:
        ctp.download_query_results(query=pki)
        ctp.parse_downloaded_xml_files(query=pki)
    for row in ctp.get_data_rows():
        fh.write("%s\n" % row)
    fh.close()


if __name__ == "__main__":
    main()
