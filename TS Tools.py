"""
A compilation of modules to assist in local processes during typesetting.
"""

from lib import welcome_sequence, hor_bar
from mod_01 import get_translations
from mod_03 import process_rev_file
from mod_04 import rename_files
from mod_05 import compile_to_pdf

# App variables
app_name = "Typesetting Tools"
app_ver = "1.00.01"
date = "28 Dec 2025"
email = "tlcpineda.projects@gmail.com"
options = [
    {
        'menu': '[S]crape translations',
        'shortkey': 'S',
        'func': get_translations,
    },
    {
        'menu': '[M]ark files for revision',
        'shortkey': 'M',
        'func': process_rev_file,
    },
    {
        'menu': '[R]ename files',
        'shortkey': 'R',
        'func': rename_files,
    },
    {
        'menu': '[C]ompile PSD',
        'shortkey': 'C',
        'func': compile_to_pdf
    },
    {
        'menu': "E[X]it and close window",
        'shortkey': 'X'
    }
]

def display_menu():
    print("")

    hor_bar(60, "MENU")

    for option in options:
        print(f"{" ":5}{option['menu']}")

    hor_bar(60)

    print("\n>>> Select an option ...")


if __name__ == "__main__":
    welcome_sequence([
        app_name,
        f"ver {app_ver} {date}",
        email,
    ])

    confirm_exit = False

    while not confirm_exit:
        display_menu()
        user_input = None

        while not user_input:
            resp = input(">>> ").upper()

            if resp in [option['shortkey'] for option in options]: user_input = resp

        if user_input == 'X':
            hor_bar(60, "CLOSING DOWN ...")
            confirm_exit=True
        else:
            print("")

            selected_option = [option for option in options if option['shortkey'] == user_input][0]
            func_selected = selected_option['func'] # requires input_path

            hor_bar(60, f"RUNNING : {func_selected.__name__}()")
            func_selected()
            hor_bar(60, f"COMPLETE : {func_selected.__name__}()")

