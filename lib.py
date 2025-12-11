import tkinter as tk
from tkinter import filedialog as fd
import os

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


def continue_sequence() -> str:
    proper_resp = False
    resp = "C"

    while not proper_resp:
        print("\n>>> Select an option :"
              "\n>>>  [C]ontinue with another chapter ?"
              "\n>>>  E[X]it and close the window ?")

        resp = input(">>> ").upper()

        proper_resp = True if resp in ["C", "X"] else False

    return resp


def display_error(tag: str, message: str, exception: Exception) -> None:
    print(f"\n<=> [{tag}] {message}"
          f"\n<=>  {exception}")