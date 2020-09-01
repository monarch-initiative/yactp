import requests
import zipfile
import time
import glob
import os

from .ct_xml_parser import ClinicalTrialsXmlParser


class ClinicalTrialsParser:

    def __init__(self):
        """
        Sets up the environment if necessary
        We create a download directory for the data
        Each medication goes into its own subdirectory there
        """
        self.datadir = 'ct_data'
        self.query_dir = None
        self.header = ClinicalTrialsXmlParser.get_tsv_header()
        self.data_rows = []
        if not os.path.exists(self.datadir):
            os.makedirs(self.datadir)

    def download_query_results(self, query, count=10000):
        query_dir = os.path.join(self.datadir, query)
        self.query_dir = query_dir
        if os.path.exists(query_dir):
            print("%s exists already, skipping download" % query_dir)
        else:
            os.makedirs(query_dir)
        base_url = 'https://clinicaltrials.gov/ct2/download_studies?term=%s&down_count=%d&down_format=csv' % (
        query, count)
        save_path = os.path.join(query_dir, 'archive.zip')

        if not os.path.exists(save_path):
            r = requests.get(base_url, stream=True)
            chunk_size = 128
            with open(save_path, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    fd.write(chunk)
        # check if one or more XML files already exists. If so, we will assume that
        # all relevant files have been extracted already
        for root, dirs, files in os.walk(query_dir):
            for filename in files:
                if filename.endswith("xml"):
                    print("XML files in %s already extracted" % query_dir)
                    return
        with zipfile.ZipFile(save_path, 'r') as zip_ref:
            zip_ref.extractall(query_dir)
        return

    def parse_downloaded_xml_files(self):
        if self.query_dir is None:
            print("Cannot parse XML files because there is no saved directory")
            return
        print(ClinicalTrialsXmlParser.get_tsv_header())
        for root, dirs, files in os.walk(self.query_dir):
            for filename in files:
                if filename.endswith("xml"):
                    xmlpath = os.path.join(self.query_dir, filename)
                    parser = ClinicalTrialsXmlParser(xmlpath)
                    self.data_rows.append(parser.get_tsv_row())

    def get_header(self):
        return self.header

    def get_data_rows(self):
        return self.data_rows
