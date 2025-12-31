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

from lib import (
    continue_sequence,
    display_message,
    display_path_desc,
    identify_path,
    welcome_sequence,
)

# Module variables
mod_name = "PDF Comments Scraper"
mod_ver = "2"
date = "18 Dec 2025"
email = "tlcpineda.projects@gmail.com"
csv_name = "translations.csv"  # The filename of the output CSV file
textbox_dim_dst = [
    dim * 72 for dim in [1.25, 1.75]
]  # width x height in inches; converted to points.
psd_folder = "2 TYPESETTING"


def get_translations() -> None:
    """
    Scrape PDF file for comments.
    """
    print(">>> Select a PDF file to scrape ...")

    path = identify_path("file")

    if not path:
        print("\n<=> No file selected.")
        return

    input_path = os.path.normpath(path)  # Normalise path.
    dirname, filename = display_path_desc(input_path, "file")

    header = ["page_num", "x0", "y0", "w_box", "h_box", "text"]
    data_rows = []

    # User input for right-to-left reading order
    print("\n>>> Sort comments according to Japanese reading order (RTL) ?")

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

    print(f"\n<=> RTL sort order will{' ' if rtl else ' not '}be applied.")

    try:
        doc = fitz.open(input_path)
        col_size = [6, 10]

        print("\n<=> Summary of Retrieved Comments :")
        print(f"<=> | {'Page':>{col_size[0]}} | {'Comments':>{col_size[1]}} |")

        for page_index, page in enumerate(doc.pages()):
            page_comments = []
            page_num = page_index + 1
            page_marker = f"{page_num:02}X"

            # Get the transformation matrix used in embedding the image onto the page.
            img_props = fetch_img_props(page)
            w, h, x_off, y_off = (
                img_props["width"],
                img_props["height"],
                img_props["x_off"],
                img_props["y_off"],
            )

            page_rect = page.rect  # From PDF page
            page_width, page_height = page_rect.width, page_rect.height
            types = [0, 2]  # PDF_ANNOT_TEXT, PDF_ANNOT_FREE_TEXT
            annots = list(page.annots(types=types))

            def norm_dim(dim, dim1):
                return (dim[0] / dim1[0], dim[1] / dim1[1])

            for annot in annots:
                annot_tl = annot.rect.top_left
                x0, y0 = annot_tl.transform(
                    fitz.Matrix(w / page_width, 0, 0, h / page_height, -x_off, -y_off)
                )
                x0_norm, y0_norm = norm_dim((x0, y0), (w, h))
                w_norm, h_norm = norm_dim(textbox_dim_dst, (w, h))
                comment = clean_up(annot.info["content"])

                # Ensure that value is in [0.01, 0.99]; 1% easement
                def clamp(dim):
                    return max(0.01, min(dim, 0.99))

                page_comments.append(
                    [
                        page_marker,
                        clamp(x0_norm),
                        clamp(y0_norm),
                        int(
                            round(y0_norm / 0.05, 2)
                        ),  # bin, used in sorting vertically.
                        f"{w_norm:g}",
                        f"{h_norm:g}",
                        comment,
                    ]
                )

            data_rows = data_rows + sort_rtl(
                page_comments, rtl
            )  # Append sorted page comments to final list.

            print(
                f"<=> | {page_num:>{col_size[0]}} | {len(annots) or '-':>{col_size[1]}} |"
            )

        doc.close()
        write_to_csv(dirname, [header] + data_rows)

    except Exception as e:
        display_message("ERROR", f'Error processing "{filename}"', f"{e}")


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

    rep_dict = {"\n": " <>", "\r": " <>", "«": '"', "»": '"'}

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
    sorted_data = sorted(page_data, key=lambda x: (-x[3], x[1] * rtl))

    # Remove "bin" (index 3)), and truncate x0, y0 to (at most) 6 decimal places.
    return list(map(lambda x: [x[0], f"{x[1]:g}", f"{x[2]:g}"] + x[4:], sorted_data))


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

        display_message("SUCCESS", f"{len(data) - 1} comments written to {csv_name}.")

        display_path_desc(csv_path, "file")

    except Exception as e:
        display_message("ERROR", f"Error writing to CSV file {csv_name}.", f"{e}")


def fetch_img_props(page: fitz.Page) -> dict:
    img_list = page.get_images(full=True)

    if img_list:
        # Get the image with the maximum area.
        img = max(img_list, key=lambda image: image[2] * image[3])

        bbox, matrix = page.get_image_rects(img[0], transform=True)[0]

        """
        Matrix of the image; to be used in processing the coordinates of the comments.
        Elements of the matrix: Matrix(a, b, c, d, e, f)
            a - scaling in x-direction, width of the bbox
            b - 0 value expected; no shearing along y-direction
            c - 0 value expected; no shearing along x-direction
            d - scaling in y-direction, height of the bbox
            e - horizontal translation
            f - vertical translation
        """
        img_width, b, c, img_height, x_off, y_off = matrix

        return {
            "width": img_width,
            "height": img_height,
            "x_off": x_off,
            "y_off": y_off,
        }

    else:
        display_message("ERROR", "No image found on page.")

        return {}


if __name__ == "__main__":
    welcome_sequence([mod_name, f"ver {mod_ver} {date}", email])

    print(input("\n>>> Press enter to continue ..."))

    confirm_exit = False

    while not confirm_exit:
        get_translations()
        confirm_exit = continue_sequence()
