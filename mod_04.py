"""
Rename files in a folder, either by appending page markers (##X), or removing it.
"""
import os
from lib import welcome_sequence, identify_path, display_path_desc, continue_sequence, display_message, process_pathname

# Module variables
mod_name = "Rename PSD Files"
mod_ver = "1"
date = "14 Dec 2025"
email = "tlcpineda.projects@gmail.com"
# FUTURE Prefix language code to filename.

def rename_files() -> None:
    """
    Rename PSD files depending on append or remove method.
    """
    print(">>> Select PSD folder ...")

    path = identify_path("folder")

    if not path:
        print("\n<=> No folder selected.")
        return

    input_path = os.path.normpath(path)   # Normalise path.
    parent, base = display_path_desc(input_path, "folder")

    if not os.listdir(input_path):
        display_message(
            "ERROR",
            f"Folder \"{base}\" is empty."
        )

        return

    print(f"\n>>> Select an option to rename files ...")    # User input whether to append or remove page markers.

    method = None

    while method is None:
        print(">>>  [A]ppend page markers (##X).")  # process_pathname case 1
        print(">>>  [R]emove page markers (##X, ##).") # process_pathname case 3
        method = input(">>> ").upper()

        if method not in ["A", "R"]:
            method = None
            print("<=> Select from the options : [A, R]\n")

    method_case = {"A": 1, "R": 3,}

    print(f"\n<=> Page markers to be {"appended to" if method == "A" else "removed from"} PSD files.")

    try:
        process_pathname(method_case[method], input_path)
        display_message(
            "SUCCESS",
            f"Page markers {"appended to" if method == "A" else "removed from"} PSD files."
        )

    except Exception as e:
        display_message(
            "ERROR",
            "File renaming failed.",
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
        rename_files()
        confirm_exit =  continue_sequence()

