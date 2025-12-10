import os
import lib
import fitz

from lib import identify_path

"""
Takes a PDF file with comments as input.
Saves each comment in a CSV file with the following parameters :
    {page_num}X - PDF page number; corresponds to a PSD file;
    {x0, y0} - top-left corner of the comment, normalised with respect to the dimensions of the PDF page
    {w, h} - width and height of the comment box, normalised with respect to the dimensions of the PDF page
    {text} - text of the comment
"""

def process_file(filepath: str) -> None:
    num_pages


# Global variables
mod_name = "PDF Comments Scraper"
mod_ver = "1"
date = "10 Dec 2025"
email = "tlcpineda.projects@gmail.com"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lib.welcome_sequence([
        mod_name,
        f"ver {mod_ver} {date}",
        email
    ])

    print(input("\n>>> Press enter to continue ..."))

    confirm_exit = False

    while not confirm_exit:
        print("\n>>> Select a PDF file to scrape ...")

        path = identify_path("file")

        if path:
            filename = os.path.basename(path)

            print(f"\n<=> File selected : {filename}")

            process_file(path)
        else:
            print("\n<=> No file selected.")

        if lib.continue_sequence() == "X":
            confirm_exit = True

            print("\n<=> Closing down ...")
        else:
            confirm_exit = False

            print("\n<=> Restarting ...")

