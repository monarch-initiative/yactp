import xml.etree.ElementTree as ET


class ClinicalTrialsXmlParser:

    def __init__(self, xmlfile, query):
        print("Parsing from ", xmlfile)
        self.xmlfile = xmlfile
        self.query = query
        tree = ET.parse(xmlfile)
        self.N_A = 'n/a'
        self.root = tree.getroot()
        if self.root.tag != 'clinical_study':
            raise ValueError("Bad root element (not clinical_study): ", self.root.tag)
        self.org_study_id = self._get_nested_element('id_info', 'org_study_id')
        self.nct_id = self._get_nested_element('id_info', 'nct_id')
        brief_title = self._get_element('brief_title')
        if len(brief_title) < 200:
            self.brief_title = brief_title
        else:
            self.brief_title = brief_title[0:200] + "(truncated at 200 chars)"
        self.start_date = self._get_element('start_date')
        self.completion_date = self._get_element('completion_date')
        self.phase = self._get_element('phase')
        self.condition = self._get_element('condition')
        self.intervention_type = self._get_nested_element('intervention',
                                                          'intervention_type')  # within intervention element
        self.intervention_name = self._get_nested_element('intervention', 'intervention_name')
        self.mesh_term_list = self._get_nested_list('condition_browse',
                                                    'mesh_term')  # within intervention_browse element
        self.mesh_text = ";".join(self.mesh_term_list)

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

    def _get_nested_list(self, parent_name, name):
        parent_elem = self.root.find(parent_name)
        if parent_elem is None:
            return [self.N_A]
        else:
            items = []
            for child in parent_elem:
                items.append(child.text)
            return items

    @classmethod
    def get_tsv_header(cls):
        elems = ["query", "org_study_id", "nct_id", "brief_title", "start_date", "completion_date", "phase",
                 "condition", "intervention_type", "intervention_name", "mesh"]
        return "\t".join(elems)

    def get_tsv_row(self):
        elems = [self.query, self.org_study_id, self.nct_id, self.brief_title, self.start_date, self.completion_date,
                self.phase, self.condition, self.intervention_type, self.intervention_name, self.mesh_text]
        return "\t".join(elems)
