import argparse
import os
from ctparser import CtStudy, CtStudyAggregator
from collections import defaultdict
from typing import List, Dict

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

parser.add_argument('-m',
                       '--mesh',
                       type=str,
                       required=True,
                       help='path to MeSH file created by meshSparql.py')

# Execute the parse_args() method
args = parser.parse_args()

input_path = args.input
mesh_path = args.mesh


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


def get_mesh_dictionary(path: str) -> Dict:
    meshd = defaultdict(str)
    if not os.path.exists(path):
        raise FileNotFoundError("Could not find MeSH dictionary at %s" % path)
    with open(path) as f:
        for line in f:
            fields = line.rstrip().split("\t")
            if len(fields) != 2:
                raise ValueError("Malformed MeSH line: ", line)
            meshid = fields[0]
            meshlabel = fields[1]
            meshd[meshlabel] = meshid
    print("[INFO] We found %d MeSH items" % len(meshd))
    return meshd



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
    summaries = []
    protein_kinase_inhibitors = get_kinase_list(args.input)
    mesh_dict = get_mesh_dictionary(mesh_path)
    fh = open('clinical_trials_pki_studies.tsv', 'wt')
    fh.write("%s\n" % CtStudy.get_tsv_header())
    for pki in protein_kinase_inhibitors:
        ctp = ClinicalTrialsParser()
        ctp.download_query_results(query=pki)
        ctp.parse_downloaded_xml_files(query=pki)
        studies = ctp.get_studies()
        aggregator = CtStudyAggregator(studies=studies, mesh_dictionary=mesh_dict)
        summaries.extend(aggregator.get_sorted_studies())
    for study in studies:
        fh.write("%s\n" % study.get_tsv_row())
    fh.close()
    print_stats(studies=studies, outname="yactp-stats.txt")
    fh = open('clinical_trials_by_phase.tsv', 'wt')
    fh.write("neoplasm\tmesh_id\tdrug\tphase\tstart_date\tcompletion_date\tnct_id\n")
    for s in summaries:
        fh.write(s + "\n")


if __name__ == "__main__":
    main()
