from .ct_study import CtStudy


class DiseaseMedPair:
    """
    Represents a study on a disease in which a certain medication was investigated.
    """
    def __init__(self, disease: str, meshid:str, medication: str) -> None:
        self._disease = disease
        self._meshid = meshid
        self._medication = medication
        self._phase1_start = [] 
        self._phase2_start = [] 
        self._phase3_start = [] 
        self._phase4_start = [] 
        self._phase1_ncit = [] 
        self._phase2_ncit = [] 
        self._phase3_ncit = [] 
        self._phase4_ncit = [] 
        self._phase_unknown_start = [] 
        self._phase_unknown_ncit = [] 

    @property
    def key(self):
        return "%s-%s" % (self._meshid, self._medication)

    def add_study(self, study: CtStudy):
        phase = study.highest_phase
        if phase < 0:
            self._phase_unknown_start.append(study.start_year)
            self._phase_unknown_ncit.append(study.nct_id)
        elif phase == 1:
            self._phase1_start.append(study.start_year)
            self._phase1_ncit.append(study.nct_id)
        elif phase == 2: 
            self._phase2_start.append(study.start_year)
            self._phase2_ncit.append(study.nct_id)
        elif phase == 3: 
            self._phase3_start.append(study.start_year)
            self._phase3_ncit.append(study.nct_id)
        elif phase == 4: 
            self._phase4_start.append(study.start_year)
            self._phase4_ncit.append(study.nct_id)
        else:
            # should never happen
            raise ValueError("Invalid phase:", phase)


    def get_row(self, phase, starts, ncits):
        items = []
        minyear = min(starts)
        maxyear = max(starts)
        ncit = ";".join(ncits)
        items.append(self._disease)
        items.append(self._meshid)
        items.append(self._medication)
        items.append(phase)
        items.append(str(minyear))
        items.append(str(maxyear))
        items.append(ncit)
        return "\t".join(items)

    def get_summary(self):
        rows = []
        if len(self._phase1_start) > 0:
            rows.append(self.get_row("Phase 1", self._phase1_start, self._phase1_ncit))
        if len(self._phase2_start) > 0:
            rows.append(self.get_row("Phase 2", self._phase2_start, self._phase2_ncit))
        if len(self._phase3_start) > 0:
            rows.append(self.get_row("Phase 3", self._phase3_start, self._phase3_ncit))
        if len(self._phase4_start) > 0:
            rows.append(self.get_row("Phase 4", self._phase4_start, self._phase4_ncit))
        if len(self._phase_unknown_start) > 0:
            rows.append(self.get_row("Phase Unknown", self._phase_unknown_start, self._phase_unknown_ncit))
        return rows

