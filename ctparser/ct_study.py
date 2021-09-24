from typing import List
import re


class CtStudy:
    def __init__(self, query: str, org_study_id: str, nct_id: str, brief_title: str,
                 start_date: str, completion_date: str, phase: str,
                 condition: str, intervention_type: str,
                 intervention_name: str, mesh_term_list: List[str]) -> None:
        super().__init__()
        self._query = query
        self._org_study_id = org_study_id
        self._nct_id = nct_id
        if len(brief_title) < 200:
            self._brief_title = brief_title
        else:
            self._brief_title = brief_title[0:200] + "(truncated at 200 chars)"
        self._start_date = start_date
        self._completion_date = completion_date
        regex = "[12]\d{3,3}"
        match = re.findall(regex, start_date)
        if not match:
            print("Could not find year in start date '%s'" % start_date)
            self._start_year = None
        else:
            self._start_year = int(match[0])
        match = re.findall(regex, completion_date)
        if not match:
            self._completion_year = None
        else:
            self._completion_year = int(match[0])
        self._phase = phase
        self._highest_phase = self._calculate_highest_phase(phase)
        self._condition = condition
        self._intervention_type = intervention_type
        self._intervention_name = intervention_name
        self._mesh_term_list = mesh_term_list
        self._mesh_text = ";".join(self.mesh_term_list)

    @classmethod
    def get_tsv_header(cls):
        elems = ["query", "org_study_id", "nct_id", "brief_title", "start_date", "completion_date", "phase",
                 "condition", "intervention_type", "intervention_name", "mesh"]
        return "\t".join(elems)

    def get_tsv_row(self):
        elems = [self._query, self._org_study_id, self._nct_id, self._brief_title, self._start_date,
                 self._completion_date,
                 self._phase, self._condition, self._intervention_type, self._intervention_name, self._mesh_text]
        return "\t".join(elems)

    def _calculate_highest_phase(self, phase):
        """
        Phase information can be recorded as either Phase I or Phase I/Phase II
        """
        if not "/" in phase:
            # In this case, it must be one of the following to be well formed
            if phase == "Phase 1":
                return 1
            elif phase == "Early Phase 1":
                return 1
            elif phase == "Phase 2":
                return 2
            elif phase == "Phase 3":
                return 3
            elif phase == "Phase 4":
                return 4
            else:
                raise ValueError("Did not recognize Phase '%s'" % phase)
        else:
            # We check in order of highest priority
            if "Phase 4" in phase:
                return 4
            elif "Phase 3" in phase:
                return 3
            elif "Phase 2" in phase:
                return 2
            elif "Phase 1" in phase:
                return 1
            elif "N/A" == phase or "n/a" == phase:
                return -1
            else:
                raise ValueError("Did not recognize Phase '%s'" % phase)

    @property
    def query(self):
        return self._query

    @property
    def org_study_id(self):
        return self._org_study_id

    @property
    def nct_id(self):
        return self._nct_id

    @property
    def brief_title(self):
        return self._brief_title

    @property
    def start_date(self):
        return self._start_date

    @property
    def completion_date(self):
        return self._completion_date

    @property
    def start_year(self):
        return self._start_year

    @property
    def completion_year(self):
        return self._completion_year

    @property
    def phase(self):
        return self._phase

    @property
    def highest_phase(self):
        return self._highest_phase

    @property
    def condition(self):
        return self._condition

    @property
    def intervention_type(self):
        return self._intervention_type

    @property
    def intervention_name(self):
        return self._intervention_name

    @property
    def mesh_term_list(self):
        return self._mesh_term_list

    @property
    def mesh_text(self):
        return self._mesh_text

    def has_valid_phase(self):
        return self._highest_phase > 0

    def has_valid_start_year(self):
        return self._start_year is not None
