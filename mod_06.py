"""

"""
import os
from operator import not_

from PIL import Image
from PIL.ImageSequence import Iterator

from lib import welcome_sequence, identify_path, display_path_desc, continue_sequence, display_message

# Module variables
mod_name = "Compile PSD to PDF"
mod_ver = "1"
date = "19 Dec 2025"
email = "tlcpineda.projects@gmail.com"
psd_folder = "2 TYPESETTING"
lang_dict = {
    'kh': 'Khmer',
    'hi': 'Hindi'
}   # FUTURE To be harmonised with work title codes:  etc "2025-Q4-KH-B5-34", "2025-Q4-HI-B2-12", and title log.

def compile_to_pdf(input_folder):
    # Get and sort files from folder
    files = [f for f in os.listdir(input_folder) if (' ' in f and os.path.splitext(f)[1].lower() == '.psd')]

    try:
        files.sort(key=get_sort_number)
    except ValueError:
        files.sort()

    if not files:
        print("No PSD files found.")
        return

    # Initialise the generator
    # Slice [1:]; first image is handled by the save() call, as anchor
    img_stream = image_generator(input_folder, files[1:])
    first_path = os.path.join(input_folder, files[0])

    output_filepath = gen_out_filepath(input_folder)

    try:
        with Image.open(first_path) as first_img:
            base_img = first_img.convert("RGB")

            # The "save" function pulls from the generator one by one
            base_img.save(
                output_filepath,
                "PDF",
                resolution=72.0,
                save_all=True,
                append_images=img_stream
            )

        display_message(
            "SUCCESS",
            f"{len(files)} PSD files compiled as PDF."
        )
        display_path_desc(output_filepath, "file")

    except Exception as e:
        display_message(
            "ERROR",
            "Failed to create PDF.",
            f"{e}"
        )


def get_sort_number(filename: str):
    """

    :param filename:
    :return:
    """
    name_only = filename.lower().replace('.psd', '')
    num_str = "".join([char for char in name_only if char.isdigit()])

    return int(num_str) if num_str else filename


def image_generator(folder: str, files: list) -> Iterator:
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
                    f"Converting {filename} ...",
                )

                yield img.convert("RGB")

        except Exception as e:
            display_message(
                "ERROR",
                f"Error processing {filename}",
                f"{e}"
            )


def gen_out_filepath(folder_path: str) -> str:
    """

    :param folder_path: The path pointing to the parent folder of the PSD folder.
    :return: The PDF path where the images will be converted to
    """
    parent = os.path.dirname(folder_path)
    title_folder, ch_folder = parent.split("\\")[-2:]

    title_split = title_folder.split(" ")
    lang_iso = title_split[0].split('-')[2].lower()
    ch_num = ch_folder.replace('CH', '')
    title = ' '.join(title_split[1:]).title()
    pdf_name = f"{title}_{lang_dict[lang_iso]} CH_{ch_num}_For TP Check.pdf"

    return os.path.join(parent, pdf_name)


if __name__ == "__main__":
    # module_06_psd_to_pdf_streaming("./chapter_folder", "QA_Reference_72dpi.pdf")
    # gen_out_filepath(psd_folder)

    while False:
        welcome_sequence([
            mod_name,
            f"ver {mod_ver} {date}",
            email
        ])

        print(input("\n>>> Press enter to continue ..."))

        confirm_exit = False

        while not confirm_exit:
            print(">>> Select a PDF file to scrape ...")

            path = identify_path("folder")

            if path:
                # get psd_folder
                compile_to_pdf(path)
            else:
                print("\n<=> No folder selected.")

            if continue_sequence() == "X":
                confirm_exit = True

                print("\n<=> Closing down ...")
            else:
                confirm_exit = False

                print("\n<=> Restarting ...")

