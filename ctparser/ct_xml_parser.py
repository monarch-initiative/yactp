
import xml.etree.ElementTree as ET

class ClinicalTrialsXmlParser:

    def __init__(self, xmlfile):
        print("Parsing from " , xmlfile)
        self.xmlfile = xmlfile
        tree = ET.parse(xmlfile)
        self.N_A = 'n/a'

        # get root element
        self.root = tree.getroot()
        if self.root.tag != 'clinical_study':
            raise ValueError("Bad root element (not clinical_study): ", self.root.tag)
        self.org_study_id = self._get_nested_element('id_info', 'org_study_id')
        self.nct_id = self._get_nested_element('id_info', 'nct_id')
        self.brief_title = self._get_element('brief_title')
        self.start_date = self._get_element('start_date')
        self.completion_date = self._get_element('completion_date')
        self.phase = self._get_element('phase')
        self.condition = self._get_element('condition')
        self.intervention_type = self._get_nested_element('intervention', 'intervention_type' ) # within intervention element
        self.intervention_name = self._get_nested_element('intervention', 'intervention_name')
        self.mesh_term = self._get_nested_element('intervention_browse', 'mesh_term') # within intervention_browse element




    def _get_nested_element(self, parent_name, name):
        parent_elem = self.root.find(parent_name)
        if parent_elem is None:
            return self.N_A
        elem = parent_elem.find(name)
        if elem is None:
            return self.N_A
        else:
            return elem.text

    def _get_element(self, name):
        elem = self.root.find(name)
        if elem is None:
            return 'n/a'
        else:
            return elem.text

    def _get_org_study_and_ncit(self):
        id_info_elem = self._get_element('id_info')
        id_elem_text = self.N_A
        ncit_id_text = self.N_A
        if id_info_elem is None:
            print("[WARN] %s had not id_info element" % self.xmlfile)
        else:
            id_elem = id_info_elem.find('org_study_id')
            if id_elem is not None:
                if id_elem == -1:
                    id_elem_text = self.N_A
                else:
                    id_elem_text = str(id_elem)
            ncit_elem = id_info_elem.find('nct_id')
            if ncit_elem is not None:
                if ncit_elem == -1:
                    ncit_id_text = self.N_A
                else:
                    ncit_id_text = ncit_elem.text
        return id_elem_text, ncit_id_text

    @classmethod
    def get_tsv_header(cls):
        elems = ["org_study_id" , "nct_id", "brief_title", "start_date", "completion_date", "phase",
                 "condition", "intervention_type", "intervention_name", "mesh_term"]
        return "\t".join(elems)

    def get_tsv_row(self):
        elems = [self.org_study_id , self.nct_id, self.brief_title,self.start_date,  self.completion_date, self.phase,
                 self.condition, self.intervention_type, self.intervention_name, self.mesh_term]
        return "\t".join(elems)


