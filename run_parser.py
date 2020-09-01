from ctparser import ClinicalTrialsParser


def main():
    ctp = ClinicalTrialsParser()
    ctp.download_query_results(query='lapatinib', count=2)
    ctp.parse_downloaded_xml_files()
    print(ctp.get_header())
    for row in ctp.get_data_rows():
        print(row)


if __name__ == "__main__":
    main()
