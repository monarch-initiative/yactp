import argparse
import os
from ctparser import CtStudy, CtStudyAggregator
from collections import defaultdict
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



def print_stats(studies: List, outname) -> None:
    fh = open(outname, 'wt')
    studycounts = defaultdict(int)
    medcounts = defaultdict(int)
    for study in studies:
        studycounts[study.highest_phase] += 1
        medcounts[study.intervention_name] += 1
    for k,v in studycounts.items():
        fh.write("Phase %d n=%d\n" % (k,v))
    for k,v in medcounts.items():
        fh.write("%s: %d studies\n" % (k,v))



def main():
    studies = []
    
    protein_kinase_inhibitors = get_kinase_list(args.input)
    fh = open('clinical_trials_pki_studies.tsv', 'wt')
    fh.write("%s\n" % CtStudy.get_tsv_header())
    for pki in protein_kinase_inhibitors:
        ctp = ClinicalTrialsParser()
        ctp.download_query_results(query=pki)
        ctp.parse_downloaded_xml_files(query=pki)
        studies = ctp.get_studies()
        aggregator = CtStudyAggregator(studies=studies)
    for study in studies:
        fh.write("%s\n" % study.get_tsv_row())
    fh.close()
    print_stats(studies=studies, outname="yactp-stats.txt")


if __name__ == "__main__":
    main()
