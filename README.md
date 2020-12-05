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


	


|  query	|  org_study_id	| nct_id| 	brief_title	| start_date| 	completion_date	phase	| condition	| intervention_type	| intervention_name| 	mesh| 
|-	|-	|-	|-	|-	|-	|-	|-	|-	|-	|-	|
afatinib|	MedOPP137	|NCT03623750	|E GFR TKI and EGF-P TI C Ombination in EGFR mutA nt NSCL C	|July 6, 2018	|August 1, 2020	|Phase 1/Phase 2|	Carcinoma, Non-Small-Cell Lung	|Drug|	EGFR-TK Inhibitor|	Carcinoma, Non-Small-Cell Lung|
afatinib	|BIBW2992 ORL|	NCT01427478	|Evaluation of Afatinib in Maintenance Therapy in Squamous Cell Carcinoma of the Head and Neck|September 2011	|November 2021|	Phase 3	|Head and Neck Squamous Cell Carcinoma|	Drug|	AFATINIB	|Carcinoma;Carcinoma, Squamous Cell;Squamous Cell Carcinoma of Head and Neck|

