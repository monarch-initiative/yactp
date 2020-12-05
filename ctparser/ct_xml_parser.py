import xml.etree.ElementTree as ET
from .ct_study import CtStudy

class ClinicalTrialsXmlParser:

    def __init__(self, xmlfile, query):
        print("Parsing from ", xmlfile)
        self.xmlfile = xmlfile
        self.N_A = 'n/a'
        self._query = query
       

    def parse(self) -> CtStudy :
        tree = ET.parse(self.xmlfile)
        root = tree.getroot()
        if root.tag != 'clinical_study':
            raise ValueError("Bad root element (not clinical_study): ", self.root.tag)
        org_study_id = self._get_nested_element(root=root, parent_name='id_info', name='org_study_id')
        nct_id = self._get_nested_element(root=root, parent_name='id_info', name='nct_id')
        brief_title = self._get_element(root=root,name='brief_title')
        start_date = self._get_element(root=root, name='start_date')
        completion_date = self._get_element(root=root, name='completion_date')
        phase = self._get_element(root=root, name='phase')
        condition = self._get_element(root=root, name='condition')
        intervention_type = self._get_nested_element(root=root, parent_name='intervention', name='intervention_type') 
        intervention_name = self._get_nested_element(root=root, parent_name='intervention', name='intervention_name')
        mesh_term_list = self._get_nested_list(root=root, parent_name='condition_browse',name='mesh_term')
        study = CtStudy(query=self._query, org_study_id=org_study_id, nct_id=nct_id, brief_title=brief_title,start_date=start_date,completion_date=completion_date,
                    phase=phase, condition=condition, intervention_type=intervention_type, intervention_name=intervention_name,
                    mesh_term_list=mesh_term_list)
        return study

        

    def _get_nested_element(self, root, parent_name, name):
        parent_elem = root.find(parent_name)
        if parent_elem is None:
            return self.N_A
        elem = parent_elem.find(name)
        if elem is None:
            return self.N_A
        else:
            return elem.text

    def _get_element(self, root, name):
        elem = root.find(name)
        if elem is None:
            return 'n/a'
        else:
            return elem.text

    def _get_nested_list(self, root, parent_name, name):
        parent_elem = root.find(parent_name)
        if parent_elem is None:
            return [self.N_A]
        else:
            items = []
            for child in parent_elem:
                items.append(child.text)
            return items

   
