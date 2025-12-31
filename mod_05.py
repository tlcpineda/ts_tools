"""
Compile PSD files contained in the selected folder into a single PDF file.
PDF filename is parsed from the parent directory of the files.
"""

import os

from PIL import Image

from lib import (
    continue_sequence,
    display_message,
    display_path_desc,
    identify_path,
    welcome_sequence,
)

# Module variables
mod_name = "Compile PSD to PDF"
mod_ver = "1"
date = "19 Dec 2025"
email = "tlcpineda.projects@gmail.com"
psd_folder = "2 TYPESETTING"
lang_dict = {
    "kh": "Khmer",
    "hi": "Hindi",
}  # FUTURE To be harmonised with title codes:  etc "2025-Q4-KH-B5-34", "2025-Q4-HI-B2-12", and title log.
filename_patterns = [
    "{TitleName_vol[3]_chap[4]_pg[3] pg[2]}.psd",
    "{TitleName_vol[3]_chap[4]_pg[3] pg[2]}X.psd",
    "{TitleName_vol[3]_chap[4]_pg[3]}.psd",
]


def compile_to_pdf():
    print(">>> Select PSD folder ...")

    path = identify_path("folder")

    if not path:
        print("\n<=> No folder selected.")
        return

    input_path = os.path.normpath(path)  # Normalise path.
    display_path_desc(input_path, "folder")

    # Get and sort PSD files from folder; only files that follow filename pattern.
    files = filter_files(input_path)

    if not files:
        print("No PSD files fit to be compiled.")
        return

    try:
        files.sort(key=get_pg_num)
    except ValueError:
        files.sort()

    # Initialise the generator
    # Slice [1:]; first image is handled by the save() call, as anchor
    img_stream = image_generator(input_path, files[1:])
    first_path = os.path.join(input_path, files[0])

    output_filepath = gen_out_filepath(input_path)

    try:
        with Image.open(first_path) as first_img:
            base_img = first_img.convert("RGB")

            # The "save" function pulls from the generator one by one
            display_message(
                "PROCESSING",
                f"Creating anchor file : {files[0]} ...",
            )

            base_img.save(
                output_filepath,
                "PDF",
                resolution=72.0,
                save_all=True,
                append_images=img_stream,
            )

        display_message("SUCCESS", f"{len(files)} PSD files compiled as PDF.")
        display_path_desc(output_filepath, "file")

    except Exception as e:
        display_message("ERROR", "Failed to create PDF.", f"{e}")


def filter_files(folder: str) -> list:
    """
    Filter files that follow the filename pattern, with the last two/three digits as the page markers.
    :param folder: The parent folder of the PSD files
    :return filtered_files: The list of filtered PSD files to be compiled
    """
    filtered_files = []

    for f in os.listdir(folder):
        if (
            os.path.splitext(f)[1].lower() == ".psd"
        ):  # Append file to return list if page_marker exists.
            page = get_pg_num(f)
            if page != 999:
                filtered_files.append(f)

    return filtered_files


def get_pg_num(filename: str) -> int:
    """
    Extract the page number from the filename.
    :param filename: The filename of the PSD file.
    :return: The page number
    """
    basename = os.path.splitext(filename)[0]
    pg_str = "".join([char for char in basename if char.isdigit()])[
        -2:
    ]  # Get the last two numeric characters.

    return (
        int(pg_str) if pg_str else 999
    )  # Return an absurdly large number if pg_str is null string.


def image_generator(folder: str, files: list):
    """
    Opens, converts, and yields one image at a time to save memory.
    :param folder: The parent folder of the PSD file
    :param files:
    :return:
    """
    for filename in files:
        filepath = os.path.join(folder, filename)

        try:
            with Image.open(filepath) as img:
                display_message(
                    "PROCESSING",
                    f"Adding file : {filename} ...",
                )

                yield img.convert("RGB")

        except Exception as e:
            display_message("ERROR", f"Error processing file : {filename}", f"{e}")


def gen_out_filepath(folder_path: str) -> str:
    """
    Generate the complete path and filename to be used by the PDF file.
    :param folder_path: The path pointing to the parent folder of the PSD folder.
    :return: The PDF path where the images will be converted to
    """
    parent = os.path.dirname(folder_path)
    title_folder, ch_folder = parent.split(os.sep)[-2:]
    title_split = title_folder.split(" ")
    lang_iso = title_split[0].split("-")[2].lower()
    ch_num = ch_folder.replace("CH", "")
    title = " ".join(
        title_split[1:]
    )  # Assume that the title is already properly capitalised.
    pdf_name = f"{title}_{lang_dict[lang_iso]} CH {ch_num}_For TP Check.pdf"
    out_filepath = os.path.join(parent, pdf_name)

    if os.path.exists(out_filepath):
        out_filepath = os.path.join(parent, f"COPY {pdf_name}")

    return out_filepath


if __name__ == "__main__":
    welcome_sequence([mod_name, f"ver {mod_ver} {date}", email])

    print(input("\n>>> Press enter to continue ..."))

    confirm_exit = False

    while not confirm_exit:
        compile_to_pdf()
        confirm_exit = continue_sequence()
