"""
Takes a PDF file with comments as input.
Identifies pages with comments, ie possible revisions, and mark corresponding PSD file
Rename folder from "2 TYPESETTING" TO "6 FINAL PSD"
"""
import fitz
import os

from lib import welcome_sequence, identify_path, display_path_desc, continue_sequence, display_message, mark_for_rev, \
    rename_path

# Global variables
mod_name = "Revisions"
mod_ver = "1"
date = "12 Dec 2025"
email = "tlcpineda.projects@gmail.com"
folder_name0 = "2 TYPESETTING"
folder_name1 = "6 FINAL PSD"

def process_rev_file(filepath: str) -> None:
    """
    Create a list of pages with comments, or markings, for revisions.
    :param filepath: The path pointing to the PDF file marked with revisions
    :return:
    """
    dirname, filename = display_path_desc(filepath, "file")

    try:
        doc = fitz.open(filepath)
        col_size = [6, 10]

        print("\n<=> Summary :")
        print(f"<=> | {"Page":>{col_size[0]}} | {"Comments":>{col_size[1]}} |")

        pages_marked = []

        for page_index, page in enumerate(doc):
            page_num = page_index + 1

            # Select all pages with at least one annotation (usually of type [0, 2, 13).
            annots = list(page.annots())

            if len(annots)>0: pages_marked.append(f"{page_num:02}")

            print(f"<=> | {page_num:>{col_size[0]}} | {len(annots) or "-":>{col_size[1]}} |")

        folder0 = mark_for_rev(dirname, folder_name0, pages_marked) # Mark files for revision.

        len_pages = len(pages_marked)
        message = "No revisions required for this chapter." # Default message for zero annotations.

        if len_pages>0: message = f"{len_pages} file{"s" if len_pages>1 else ""} marked for revision."

        display_message(
            "SUCCESS",
            message
        )

        folder1 = os.path.join(dirname, folder_name1)

        if folder0 != folder1:
            rename_path(folder0, folder1, "folder")
        else:
            display_message(
                "ERROR",
                "Cannot rename folder."
            )

    except Exception as e:
        display_message(
            "ERROR",
            "Failed marking files for revision.",
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
        print(">>> Select a PDF file marked with revisions ...")

        path = identify_path("file")

        if path: process_rev_file(path)
        else: print("\n<=> No file selected.")

        if continue_sequence() == "X":
            confirm_exit = True

            print("\n<=> Closing down ...")
        else:
            confirm_exit = False

            print("\n<=> Restarting ...")

