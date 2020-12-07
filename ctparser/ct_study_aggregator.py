from typing import List, Dict
from collections import defaultdict

from .ct_study import CtStudy
from .disease_med_pair import DiseaseMedPair


class CtStudyAggregator:
    """
    This class intends to aggregate studies about a given drug that have been retrieved
    by the CtXmlParser as CtStudyObjects
    """
    def __init__(self, studies: List, mesh_dictionary: Dict) -> None:
        super().__init__()
        self._studies = studies
        self._mesh_dict = mesh_dictionary
        self._disease2med_dictionary = defaultdict(list)
        for study in self._studies:
            if not study.has_valid_phase():
                continue
            if not study.has_valid_start_year():
                continue
            medication = study.query # by design, we query ClinicalStudies using medication names
            for term in study.mesh_term_list:
                if term in mesh_dictionary:
                    meshid = mesh_dictionary.get(term)
                    key = "%s-%s" % (meshid, medication)
                    if not key in self._disease2med_dictionary:
                        dmp = DiseaseMedPair(disease=term, meshid=meshid, medication=medication)
                        self._disease2med_dictionary [key] = dmp
                    dmp = self._disease2med_dictionary .get(key)
                    dmp.add_study(study)

    def get_sorted_studies(self):
        """
        Get a list of studies intended for output
        """
        rows = []
        for dmp in self._disease2med_dictionary.values():
            rows.extend(dmp.get_summary())
        return rows

