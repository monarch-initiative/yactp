# yactp
Yet Another Clinical Trials Parser


## Running yactp

The expected input file is a list of medication names, one on a line. For instance,

```
afatinib
imatinib
(...)
```

Run the script as follows
```
python parseCT.py -i <path-to-input-file>
```

For demonstration purposes, if you leave off the ``-i`` argument, the script will use a file in
the subdirectory ``kinase_data`` that contains just two medication names.


The script will generate an output file called ``clinical_trials_pki_studies``.


	

<table>
<tr><td>query</td><td>org_study_id</td><td>nct_id</td><td>brief_title</td><td>start_date</td><td>completion_date</td><td>phase</td><td>condition</td><td>intervention_type</td><td>intervention_name</td><td>	mesh</td></tr>
<tr><td>afatinib</td><td>MedOPP137</td><td>NCT03623750</td><td>E GFR TKI and EGF-P TI C Ombination in EGFR mutA nt NSCL C	</td><td>July 6, 2018</td><td>August 1, 2020</td><td>Phase 1/Phase 2</td><td>Carcinoma, Non-Small-Cell Lung</td><td>Drug</td><td>EGFR-TK Inhibitor</td><td>Carcinoma, Non-Small-Cell Lung</td></tr>
<tr><td>afatinib</td><td>BIBW2992 ORL</td><td>NCT01427478</td><td>Evaluation of Afatinib in Maintenance Therapy in Squamous Cell Carcinoma of the Head and Neck</td><td>September 2011</td><td>November 2021</td><td>	Phase 3	</td><td>Head and Neck Squamous Cell Carcinoma</td><td>	Drug|	AFATINIB</td><td>Carcinoma;Carcinoma, Squamous Cell;Squamous Cell Carcinoma of Head and Neck</td></tr>
</table>

