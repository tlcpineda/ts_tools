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
from PIL import Image

from lib import welcome_sequence, identify_path, display_path_desc, continue_sequence, display_message

# Module variables
mod_name = "PDF Comments Scraper"
mod_ver = "2"
date = "10 Dec 2025"
email = "tlcpineda.projects@gmail.com"
csv_name = "translations.csv"   # The filename of the output CSV file
textbox_dim_dst = [dim * 72 for dim in [1.25, 1.75]] # width x height in inches; converted to points.
psd_folder = "2 TYPESETTING"

def process_file(filepath: str) -> None:
    """
    Scrape PDF file for comments.
    :param filepath: The file path of the PDF file
    :return:
    """
    dirname, filename = display_path_desc(filepath, "file")

    header = [
        "page_num",
        "x0",
        "y0",
        "w_box",
        "h_box",
        "text"
    ]
    data_rows = []

    # User input for right-to-left reading order
    print(f"\n>>> Sort comments according to Japanese reading order (RTL) ?")

    rtl = None

    while rtl is None:
        print(">>>  [Y]es or Enter to apply RTL sort order.")
        print(">>>  [N]o to keep LRT sort order.")
        user_in = input(">>>  ").upper()

        if user_in not in ["Y", "N", ""]:
            print("<=> Select from the options : [Y, N, Enter]\n")
        elif user_in in ["Y", ""]:
            rtl = True
        else:
            rtl = False

    print(f"\n<=> RTL sort order will{" " if rtl else " not "}be applied.")

    try:
        # TODO insert method to mutate PDF coordinates to match PSD dimensions.
        # Fetch dimensions of PSD files in psd_folder.
        display_path_desc(os.path.join(dirname, psd_folder), "folder")
        psd_props = fetch_psd_props(os.path.join(dirname, psd_folder))

        doc = fitz.open(filepath)
        col_size = [6, 10]

        print(f"\n<=> Summary of Retrieved Comments :")
        print(f"<=> | {"Page":>{col_size[0]}} | {"Comments":>{col_size[1]}} |")

        for page_index, page in enumerate(doc.pages()):
            page_comments = []
            page_num = page_index + 1
            page_marker = f"{page_num:02}X"
            psd_dim = psd_props[page_marker]['dim']

            # TODO Determine transformation parameters PDF to PSD
            page_rect = page.rect

            print(page_rect) # branch
            page_width, page_height = page_rect.width, page_rect.height
            (x_off, y_off, width_adj, height_adj) = transforms(psd_dim, page.rect)

            types = [0, 2]  # PDF_ANNOT_TEXT, PDF_ANNOT_FREE_TEXT
            annots = list(page.annots(types=types))

            # norm_dim = lambda a0, a: (a0 / a)
            norm_dim = lambda box_dim, dim_dst: (box_dim[0] / dim_dst[0], box_dim[1] / dim_dst[1])

            for annot in annots:
                annot_rect = annot.rect
                # x0_norm = annot_rect.x0 / page_width
                # y0_norm = annot_rect.y0 / page_height

                x0_norm, y0_norm = norm_dim( (annot_rect.x0, annot_rect.y0), psd_dim)

                # Normalise dimensions of textbox.
                # w_norm, h_norm = norm_dim(textbox_dim_dst[0], page_width), norm_dim(textbox_dim_dst[1], page_height)
                w_norm, h_norm = norm_dim(textbox_dim_dst, psd_dim)


                comment = clean_up(annot.info['content'])

                page_comments.append([
                    page_marker,
                    x0_norm,
                    y0_norm,
                    int(round(y0_norm / 0.05, 2)),    # bin, used in sorting vertically.
                    f"{w_norm:.6f}",
                    f"{h_norm:.6f}",
                    comment
                ])

            data_rows = data_rows + sort_rtl(page_comments, rtl)   # Append sorted page comments to final list.

            print(f"<=> | {page_num:>{col_size[0]}} | {len(annots) or "-":>{col_size[1]}} |")

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


def fetch_psd_props(psd_dir: str) -> dict:
    """
    Retrieve the width and height, in pixels, of the working PSD files.
    :param psd_dir: Path containing the working PSD files.
    :return properties: Dictionary with key as the page maker ("##X"), and values as a dictionary {dim, res};
     dim (width, height), and res (x_res, y_res) of the working PSD files.
    """
    print(f"\n<=> Fetching PSD Dimensions ...")

    properties = {}

    for file in os.listdir(psd_dir):
        if file.lower().endswith(".psd"):
            psd_path = os.path.join(psd_dir, file)
            filename = os.path.splitext(file)[0]

            try:
                with Image.open(psd_path) as img:
                    dpi = img.info.get('dpi', (72, 72))
                    size = img.size # img.size is a tuple: (width, height)
                    properties[f"{filename.split(" ")[1]}"] = {'dim': size, 'res': dpi}

                    print(f"<=> {file} :\n"
                          f"<=>  Dimensions : {size} px\n"
                          f"<=>  Resolution : {dpi} dpi")

            except Exception as e:
                display_message(
                    "ERROR",
                    "fCould not read {file}",
                    f"{e}"
                )

    return properties


def transforms(psd_dim: tuple, pdf_rect: fitz.Rect) -> tuple:
    """

    :param psd_dim:
    :param pdf_rect:
    :return:
    """
    w_src, h_src = pdf_rect.width, pdf_rect.height
    w_dst, h_dst = psd_dim
    x_off, y_off = (w_dst - w_src) / 2, (h_dst - h_src) / 2
    # width, height = convert(w_dst, h_dst) # Convert PSD dimensions (pixels) to PDF dimensions (points)

    return (x_off, y_off, width, height)


if __name__ == '__main__':
    # d = r"C:\Users\Tristan Louie Pineda\Documents\ทำงาน\CCCI\2 PROJECTS\2025-Q3-KH-B2-12 Astra Lost in Space\CH49\2 TYPESETTING"
    # fetch_psd_props(d)

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

        if path: process_file(path)
        else: print("\n<=> No file selected.")

        if continue_sequence() == "X":
            confirm_exit = True

            print("\n<=> Closing down ...")
        else:
            confirm_exit = False

            print("\n<=> Restarting ...")

