from ctparser import ClinicalTrialsParser


def get_kinase_list():
    path = 'kinase_data/kinase_inhibitors.txt'
    protein_kinase_inhibitors = []
    with open(path) as f:
        for line in f:
            if len(line) > 1:
                protein_kinase_inhibitors.append(line.rstrip())
    return protein_kinase_inhibitors




def main():
    ctp = ClinicalTrialsParser()
    protein_kinase_inhibitors = get_kinase_list()
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
