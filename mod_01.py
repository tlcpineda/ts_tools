"""
Takes a PDF file with comments as input.
Saves each comment in a CSV file with the following parameters :
    {page_num}X - PDF page number; corresponds to a PSD file;
    {x0, y0} - top-left corner of the comment, normalised with respect to the dimensions of the PDF page
    {w, h} - width and height of the comment box, normalised with respect to the dimensions of the PDF page
    {text} - text of the comment
"""

import os
import fitz

from lib import welcome_sequence, identify_path, continue_sequence, display_error

# Global variables
mod_name = "PDF Comments Scraper"
mod_ver = "1"
date = "10 Dec 2025"
email = "tlcpineda.projects@gmail.com"
csv_name = "translations.csv"   # The filename of the output CSV file

def process_file(filepath: str) -> None:
    header = [
        "page_num",
        "x0",
        "y0",
        "w_box",
        "h_box",
        "text"
    ]
    data_rows = []
    dirname, filename = os.path.split(filepath)

    print(dirname, filename)
    print(f"\n<=> Processing file :"
          f"\n<=>  Directory : {dirname}"
          f"\n<=>  Filename  : {filename}")

    # Convert millimeters to points, for the dimensions of the text box in Photoshop.
    mm_to_pt = 72    # 72 points to 1 in (25.4 mm)
    w_box = 1.25 * mm_to_pt
    h_box = 1.75 * mm_to_pt

    try:
        doc = fitz.open(filepath)
        col_size = [4, 8]

        print("\nSummary :")
        print(f"<=> | {"Page":>{col_size[0]}} | {"Comments":>{col_size[1]}} |")

        for page_index, page in enumerate(doc):
            page_num = page_index + 1
            page_rect = page.rect
            page_width, page_height = page_rect.width, page_rect.height
            types = [0, 2]  # PDF_ANNOT_TEXT, PDF_ANNOT_FREE_TEXT
            annots = page.annots(types=types)

            # print(f"width : {page_width}, height : {page_height}")

            for annot in annots:
                annot_rect = annot.rect
                x0_norm = annot_rect.x0 / page_width
                y0_norm = annot_rect.y0 / page_height
                w_norm = annot_rect.width / page_width
                h_norm = annot_rect.height / page_height
                comment = clean_up(annot.info['content'])

                data_rows.append([
                    f"{page_num:02}X",
                    f"{x0_norm:.6f}",
                    f"{y0_norm:.6f}",
                    f"{w_norm:.6f}",
                    f"{h_norm:.6f}",
                    comment
                ])

            print(f"<=> | {page_num:>{col_size[0]}} | {len(list(annots)):>{col_size[1]}} |")

        doc.close()
        write_to_csv(dirname, [header] + data_rows)

    except Exception as e:
        display_error(
            "ERROR",
            f"Error processing \"{filename}\"",
            e
        )


def clean_up(comment: str) -> str:
    """
    Clean up the string. Remove leading, and trailing white spaces;
    replace : newline, or return characters by " <>";
    (restored later in ExtendScript as a proper newline or return character);
    guillemets, both initial and terminal, by a quotation mark; or,
    any other characters that may be defined in the future in rep_dict; and,
    multiple white spaces by a single space.
    :param comment:
    :return clean_comment:
    """
    clean_comment = comment.strip()

    rep_dict = {
        "\n": " <>",
        "\r": " <>",
        "«": "\"",
        "»": "\""
    }

    if comment:
        for key, value in rep_dict.items():
            clean_comment = clean_comment.replace(key, value)

    clean_comment = " ".join(clean_comment.split())

    return clean_comment


def write_to_csv(directory: str, data: list) -> None:



if __name__ == '__main__':
    welcome_sequence([
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
            # filename = os.path.basename(path)
            process_file(path)
        else:
            print("\n<=> No file selected.")

        if continue_sequence() == "X":
            confirm_exit = True

            print("\n<=> Closing down ...")
        else:
            confirm_exit = False

            print("\n<=> Restarting ...")

