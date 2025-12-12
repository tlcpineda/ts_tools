# Typesetting Tools
This is a collection of Python and ExtendScripts codes to assist in my manga in typesetting work in Photoshop.

Development started as standalone files something in October 2025, run either as executable files or wrapped in an action script within Photoshop, before the set-up of this GitHub account.  That is, before my old computer of 8 years crashed.

I am attempting here to recreate the modules that have helped me reduced non-essential tasks in my typesetting work, as well as finally setting up and learning the ropes in GitHub (after so much delays to do so).

Future development, as I see it, includes :
1. a purely Python-based operation, to handle local processes;
2. a Google Cloud project to handle the monitoring/movement of files in a shared Google Drive.  Monitoring is currently handled by a Google Apps Script bound to a Sheets log file; and,
3. a Teams integration to alert team members of my latest submission.


## General Workflow
One title - one or two languages. (more to be added later)


## Directory
* __mod_01.py__ (PDF Comments Scraper) - creates a CSV file containing all the comments in the PDF file.  CSV file is used in pasting the comments to respective PSD files.
* __mod_xx.jsx__ (CSV to PSD) - transfers the contents of the CSV file to corresponding PSD files.
* __mod_03.py__ (Revisions) - mark PSD down files that needs to be edited.
* __mod_xx.py__ (Rename Files) - append/remove markers to PSD filenames: ##x, x
* __mod_xx.py__ (Prepare Folders) - fetch working files, and create chapter folder/s under title/language


## Project Tags (Personal)

| Project ID | Title | Short Description |
|:--- |:--- |:--- |
| 2025-09-T-0024-P | PDF COMMENTS TO PSD PART 1 | PDF comments saved in a CSV file |
| 2025-09-T-0025-J | PDF COMMENTS TO PSD PART 2 | CSV data to PSD files |
| 2025-10-T-0027-P | COMPREHENSIVE CCCI SCRIPT | Compilation of individual modules |
