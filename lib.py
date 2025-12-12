import os
import tkinter as tk
from tkinter import filedialog as fd

def welcome_sequence(items: list):
    max_chars = len(max(items, key=len))
    line_len =  max_chars + 10 * 2
    items = [''] + items + ['']
    hor_bar = line_len * "░"

    print(hor_bar)

    for item in items:
        print(f"{item:^{line_len}}")

    print(hor_bar)


def identify_path(base_type: str) -> str:
    root = tk.Tk()
    root.withdraw()

    path = None

    match base_type:
        case "file":
            path = fd.askopenfilename(
                title="Select PDF File",
                filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
            )
        case "folder":
            path = fd.askdirectory(
                title="Select Folder"
            )

    return path


def display_file_desc(filepath: str) -> tuple:
    dirname, filename = os.path.split(filepath)
    split_dirname = dirname.split("/")
    num_levels = 3
    process_dirname = dirname if len(split_dirname) <= num_levels else f".../{"/".join(split_dirname[-3:])}"

    print(f"\n<=> Processing file :"
          f"\n<=>  Directory : {process_dirname}"
          f"\n<=>  Filename  : {filename}")

    return dirname, filename


def continue_sequence() -> str:
    proper_resp = False
    resp = "C"

    while not proper_resp:
        print("\n>>> Select an option :"
              "\n>>>  [C]ontinue with another chapter ?"
              "\n>>>  E[X]it and close this window ?")

        resp = input(">>> ").upper()

        proper_resp = True if resp in ["C", "X"] else False

    return resp


def display_message(tag: str, message: str, exception: str=None) -> None:
    print(f"\n<=> [{tag}] {message}")

    if exception:
        print(f"<=>  {exception}")

