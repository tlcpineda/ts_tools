# Typesetting Tools

This is a collection of Python and ExtendScripts codes to assist in my manga in typesetting work in Photoshop.

Development started as standalone files something in October 2025, run either as executable files or wrapped in an
action script within Photoshop, before the set-up of this GitHub account. That is, before my old computer of 8 years
crashed.

I am attempting here to recreate the modules that have helped me reduce non-essential tasks in my typesetting work, as
well as finally setting up and learning the ropes in GitHub (after so much delays to do so).

## General Workflow

One title is generally assigned to a typesetter. The main focus is to set the translated text, done by others, onto
corresponding PSD files following typesetting guidelines. Depending on assignment, typically a typesetter is assigned
two destination languages for the same title.

**Files downloaded from Shared Drive Folders**

* *ATN file* - (by title) action scripts; often title-based;
* *Read Me* - (by title) guidelines for typesetting; often title-based;
* *Working PSD Files* - (by chapter) multiple PSD files for the chapter; may or may not require additional processing, like removal
  of elements from previous workflow;
* *{Translations}.pdf* - (by chapter-language) file with comments containing the translated text;

**Files uploaded to Shared Drive Folders**

* *{Typeset}.pdf* - (by chapter-language) file with fully typeset translated text, for review by translator and
  coordinator;
* *Typeset PSD Files* - (by chapter-language) multiple PSD files for the chapter; for submission to QA, then to client;

**Initial Workflow**

1. [ ] ddd

(_more to be added later_)

## Future development

As I see it, when all the component have been recreated includes :

1. a purely Python-based comprehensive local app to handle local processes;
2. a Google Cloud integration to handle the monitoring/movement of files in a shared Google Drive, including personal
   work logs. Monitoring is currently handled by a Google Apps Script bound to a Sheets log file; and,
3. a Teams integration to alert team members of my latest submission.

## Directory

1. [*] **mod_01.py** (PDF Comments Scraper) - creates a CSV file containing all the comments in the PDF file. CSV file is
  used in pasting the comments to respective PSD files.
2. [ ] **mod_02.jsx** (CSV to PSD) - transfers the contents of the CSV file to corresponding PSD files.
3. [/] **mod_03.py** (Revisions) - mark PSD files that needs to be edited, rename parent folder.
4. [/] **mod_04.py** (Rename Files) - append/remove page markers to/from PSD filenames: ##x, ##
5. [ ] **mod_xx.py** (Prepare Folders) - fetch working files, and create chapter folder/s under title/language

## Project Tags (Personal)

| Project ID       | Title                      | Short Description                 |
|:-----------------|:---------------------------|:----------------------------------|
| 2025-09-T-0024-P | PDF COMMENTS TO PSD PART 1 | PDF comments saved in a CSV file  |
| 2025-09-T-0025-J | PDF COMMENTS TO PSD PART 2 | CSV data to PSD files             |
| 2025-10-T-0027-P | COMPREHENSIVE CCCI SCRIPT  | Compilation of individual modules |
