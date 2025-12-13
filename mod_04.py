import os
from lib import welcome_sequence, identify_path, display_path_desc, continue_sequence, display_message, process_pathname, \
    rename_path

# Module variables
mod_name = "Rename PSD Files"
mod_ver = "1"
date = "14 Dec 2025"
email = "tlcpineda.projects@gmail.com"

def rename_files(parent_path: str) -> None:
    """

    :param parent_path: The folder containing the PSD files to be renamed.
    :return:
    """

    # TODO user input whether to append or remove page markers.
    pass


if __name__ == '__main__':
    welcome_sequence([
        mod_name,
        f"ver {mod_ver} {date}",
        email
    ])

    print(input("\n>>> Press enter to continue ..."))

    confirm_exit = False

    while not confirm_exit:
        print(">>> Select PSD folder ...")

        path = identify_path("folder")

        if path: rename_files(path)
        else: print("\n<=> No file selected.")

        if continue_sequence() == "X":
            confirm_exit = True

            print("\n<=> Closing down ...")
        else:
            confirm_exit = False

            print("\n<=> Restarting ...")

