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

**Files**

* Downloaded from Shared Drive Folder
    * *ATN file* - (by title) action scripts; often title-based;
    * *Read Me* - (by title) guidelines for typesetting; often title-based;
    * *Working PSD Files* - (by chapter) multiple PSD files for the chapter; may or may not require additional
      processing, like removal of elements from previous workflow;
    * *{Translations}.pdf* - (by chapter-language) PDF file with comments containing the translated text; and,
    * *{Review}.pdf* - (by chapter-language) PDF file containing revision requests.

* Uploaded to Shared Drive Folders
    * *{Typeset}.pdf* - (by chapter-language) file with fully typeset translated text, for review by translator and
      coordinator; and,
    * *Typeset PSD Files* - (by chapter-language) multiple PSD files for the chapter; for submission to QA, then to
      client.

**Local Directory Structure**

```
+- PROJECTS
   +- Title Code 1
   |  +- CH1
   |  |  +- 6 FINAL PSD
   |  |  |  +- PSD001.psd
   |  |  |  +- PSD002.psd
   |  |  |  :
   |  |  |  :
   |  |  |  +- PSDmmm.psd
   |  |  +- {Translations}.pdf
   |  |  +- translations.csv
   |  |  +- {Typeset}.pdf
   |  |  +- {Review}.pdf
   |  +- CH2
   |  |  +- 2 TYPESETTING
   |  |  |  +- PSD001 01x.psd
   |  |  |  +- PSD002 02X.psd
   |  |  |  :
   |  |  |  :
   |  |  |  +- PSDmmm mmX.psd
   |  |  +- {Translations}.pdf
   |  |  +- translations.csv
   |  |  +- {Typeset}.pdf
   |  :
   |  :
   |  +- CHk
   :
   : 
   +- Title Code n
```

* Title Code - `{year}-Q{quarter}-{lang_code}-B{batch_num}_{title_num} {Title}`
    * `{year}` - current year when title was assigned; 4 digits;
    * `{quarter}` - current quarter of the year when title was assigned; 1 digit;
    * `{lang_code}` - ISO language code; 2 characters;
    * `{batch_num}` - project batch number; client-specified; currently 1 digit;
    * `{title_num}` - title number; client-specified; currently at most 2 digits; and,
    * `{Title}` - the official English title of the project.
* Working PSD File - `{TitleName}_{volume}_{chapter}_{page} {page_marker}.psd`
    * `{TileName}` - the official English title of the project in Pascal case;
    * `{volume}` - the volume number; 3 digits;
    * `{chapter}` - the chapter number; 4 digits;
    * `{page}` - the page number; 3 digits; and,
    * `{page_marker}` - depends on stage of processing:
        * `null` - during pre-processing, after revisions and prior to upload to shared project Drive folder;
        * `{nn}x` or `{nn}X` - during typesetting or revisions; 2 digit page number (last 2 digits of `{page}`), with
          literal "x" or "X";
        * `{nn}` - after typesetting;
* {Typeset}.pdf - `{Title} CH {chapter}_{mark}`
  * `{Title}` - to official English title of the project with proper capitalisation;
  * `{chapter}` - the chapter number; at least 1 digit; and,
  * `{mark}` - marker indicating file is for review; client-specified.

**Processing**

* Initial
    * Load *ATN file* to Photoshop.
    * Review *Read Me* file.
    * Install required font faces.
* Pre-processing
    * Clean up unnecessary elements on *Working PSD Files*; append page markers (##X) to filename.
    * Prepare chapter folder(s); fetch cleaned *Working PSD Files* from repository.
    * Scrape *{Translations}.pdf* and save to a CSV file.
* Main
    * Transfer contents of CSV file to corresponding PSD file; set to *Main* font style (as defined in chapter ATN
      file), and other settings as set in chapter *Read Me* file and general typesetting guidelines.
    * Adjust each text layer, following localisation and general typesetting guidelines.
    * Compile *Typeset PSD Files* to a single PDF file (*{Typeset}.pdf*), and submit for review.
    * Update translator and coordinator on Teams.
    * Update personal monitoring log.
* Chapter Submission
    * Address revision requests as marked on *{Review}.pdf* to *Typeset PSD Files*.
    * Upload *{Typeset PSD Files}* to designated shared Drive folder.
    * Update translator and coordinator on Teams.
    * Update personal monitoring log.
* Side processes
    * Monitor shared Drive folders for uploaded files from translator, in case translator fails to update on Teams.
    * Monitor Teams for announcements (extra work, general notice, updated guidelines, and the like).

## Future development

As I see it, when all the component have been recreated includes :

1. a purely Python-based comprehensive local app to handle local processes;
2. a Google Cloud integration to handle the monitoring/movement of files in a shared Google Drive, including personal
   work logs. Monitoring is currently handled by a Google Apps Script bound to a Sheets log file; and,
3. a Teams integration to alert team members of my latest submission.

## Directory

1. [x] **mod_01.py** (PDF Comments Scraper) - creates a CSV file containing all the comments in the PDF file. CSV file
   is used in pasting the comments to respective PSD files.
2. [x] **mod_02.jsx** (CSV to PSD) - transfers the contents of the CSV file to corresponding PSD files.
3. [x] **mod_03.py** (Revisions) - mark PSD files that needs to be edited, rename parent folder.
4. [x] **mod_04.py** (Rename Files) - append/remove page markers to/from PSD filenames: ##x, ##
5. [ ] **mod_05.py** (Prepare Folders) - fetch clean working files, and create chapter folder/s under title/language
6. [ ] **mod_06.py** (Compile PSD to PDF) - convert *{Typeset PSD Files}* to *{Typeset}.pdf* ready from submission.

## Project Tags (Personal)

| Project ID       | Title                      | Short Description                 |
|:-----------------|:---------------------------|:----------------------------------|
| 2025-09-T-0024-P | PDF COMMENTS TO PSD PART 1 | PDF comments saved in a CSV file  |
| 2025-09-T-0025-J | PDF COMMENTS TO PSD PART 2 | CSV data to PSD files             |
| 2025-10-T-0027-P | COMPREHENSIVE CCCI SCRIPT  | Compilation of individual modules |
