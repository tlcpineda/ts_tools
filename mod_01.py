"""
Takes a PDF file with comments as input.
Saves each comment in a CSV file with the following parameters :
    {page_num}X - PDF page number; corresponds to a PSD file;
    {x0, y0} - top-left corner of the comment, normalised with respect to the dimensions of the PDF page
    {w, h} - width and height of the comment box, normalised with respect to the dimensions of the PDF page
    {text} - text of the comment
"""
import csv
import os
import fitz

from lib import welcome_sequence, identify_path, continue_sequence, display_message

# Global variables
mod_name = "PDF Comments Scraper"
mod_ver = "1"
date = "10 Dec 2025"
email = "tlcpineda.projects@gmail.com"
csv_name = "translations.csv"   # The filename of the output CSV file

def process_file(filepath: str, rtl: bool) -> None:
    """
    Scrape PDF file for comments.
    :param filepath: The file path of the PDF file
    :param rtl: Whether RTL reading order will be applied
    :return:
    """
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
    split_dirname = dirname.split("/")
    num_folders = 3
    process_dirname = dirname if len(split_dirname) <= num_folders else f".../{"/".join(split_dirname[-3:])}"

    print(f"\n<=> Processing file :"
          f"\n<=>  Directory : {process_dirname}"
          f"\n<=>  Filename  : {filename}")

    try:
        doc = fitz.open(filepath)
        col_size = [6, 10]

        print("\n<=> Summary :")
        print(f"<=> | {"Page":>{col_size[0]}} | {"Comments":>{col_size[1]}} |")


        for page_index, page in enumerate(doc):
            if page_index > 0: return   # process only the first page while testing.

            page_comments = []

            page_num = page_index + 1
            page_rect = page.rect
            page_width, page_height = page_rect.width, page_rect.height
            types = [0, 2]  # PDF_ANNOT_TEXT, PDF_ANNOT_FREE_TEXT
            annots = list(page.annots(types=types))

            for annot in annots:
                annot_rect = annot.rect
                x0_norm = annot_rect.x0 / page_width
                y0_norm = annot_rect.y0 / page_height
                w_norm = 1.25 * 72 / page_width # Inches to points conversion before normalisation
                h_norm = 1.75 * 72 / page_height
                comment = clean_up(annot.info['content'])

                page_comments.append([
                    f"{page_num:02}X",
                    x0_norm,
                    y0_norm,
                    int(round(y0_norm / 0.05, 2)),    # bin, used in sorting vertically.
                    f"{w_norm:.6f}",
                    f"{h_norm:.6f}",
                    comment
                ])

            # for comment in page_comments: print(comment)
            for comment in sort_rtl(page_comments, rtl): print(comment)
            data_rows = data_rows + sort_rtl(page_comments, rtl)   # Append sorted page comments to final list.
            print(f"<=> | {page_num:>{col_size[0]}} | {len(annots):>{col_size[1]}} |")

        doc.close()
        # write_to_csv(dirname, [header] + data_rows)

    except Exception as e:
        display_message(
            "ERROR",
            f"Error processing \"{filename}\"",
            f"{e}"
        )


def clean_up(comment: str) -> str:
    """
    Clean up the string. Remove leading, and trailing white spaces;
    replace : newline, or return characters by " <>";
    (restored later in ExtendScript as a proper newline or return character);
    guillemets, both initial and terminal, by a quotation mark; or,
    any other characters that may be defined in the future in rep_dict; and,
    multiple white spaces by a single space.
    :param comment: The string to be cleaned up
    :return clean_comment: The resulting string
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


def sort_rtl(page_data: list, rtl: bool) -> list:
    """
    Sort the comments according to (x0, y0).
    :param page_data: The list of comments for the current page
    :param rtl: True follows Japanese manga reading order.
    :return: The reversed list of sorted comments; which reverts to proper order when transferred to Photoshop.
    """
    sorted_data = sorted(page_data, key=lambda x: ( -x[3], x[1] * rtl))

    # Remove "bin" (index 3)), and truncate x0, y0 to 6 decimal places.
    return list(map(lambda x: [x[0], f"{x[1]:6f}", f"{x[2]:6f}"] + x[4:], sorted_data))


def write_to_csv(directory: str, data: list) -> None:
    """
    Transfer the data to a CSV file named "translations.csv" (csv_name),
    with the file saved in the same directory as the source PDF file.
    :param directory: The parent directory of the source PDF file.
    :param data: A 2D array containing the comments in each page, with header row.
    :return: None
    """
    try:
        csv_path = os.path.join(directory, csv_name)
        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerows(data)

        display_message(
            "SUCCESS",
            f"{len(data) - 1} comments written to {csv_name}."
        )

    except Exception as e:
        display_message(
            "ERROR",
            f"Error writing to CSV file {csv_name}.",
            f"{e}"
        )


if __name__ == '__main__':
    welcome_sequence([
        mod_name,
        f"ver {mod_ver} {date}",
        email
    ])

    print(input("\n>>> Press enter to continue ..."))

    confirm_exit = False

    while not confirm_exit:
        print(">>> Select a PDF file to scrape ...")

        path = identify_path("file")

        if path:
            print(f"\n<=> File selected : {os.path.basename(path)}")
            print(f"\n>>> Sort comments according to Japanese reading order (RTL) ?")

            jp_read_order = None

            while jp_read_order is None:
                print(">>>  [Y]es or Enter to apply RTL sort order.")
                print(">>>  [N]o to keep LRT sort order..")
                jp_read_order = input(">>>  ")

                if jp_read_order.upper() not in ["Y", "N", ""]:
                    jp_read_order = None
                    print("")
                elif jp_read_order.upper() in ["Y", ""]:
                    jp_read_order = True
                else:
                    jp_read_order = False

            print(f"\n<=> RTL sort order will{" " if jp_read_order else " not "}be applied.")

            process_file(path, jp_read_order)
        else:
            print("\n<=> No file selected.")

        if continue_sequence() == "X":
            confirm_exit = True

            print("\n<=> Closing down ...")
        else:
            confirm_exit = False

            print("\n<=> Restarting ...")

