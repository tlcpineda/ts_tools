import lib
import fitz
import tkinter as tk

"""
Takes a PDF file with comments as input.
Saves each comment in a CSV file with the following parameters :
    {page_num}X - PDF page number; corresponds to a PSD file;
    {x0, y0} - top-left corner of the comment, normalised with respect to the dimensions of the PDF page
    {w, h} - width and height of the comment box, normalised with respect to the dimensions of the PDF page
    {text} - text of the comment
"""

# Global variables
mod_name = "PDF Comments Scraper"
mod_rel = "1"
date = "10 Dec 2025"
email = "tlcpineda.projects@gmail.com"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lib.welcome_sequence([
        mod_name,
        f"ver {mod_rel} {date}",
        email
    ])