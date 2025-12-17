import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import math

# Under development
def run_module_5():
    # Initialize UI environment
    root = tk.Tk()
    root.withdraw()

    # Directory Selection
    source_dir = filedialog.askdirectory(title="Select Source Folder")
    dest_dir = filedialog.askdirectory(title="Select Destination Folder")

    if not source_dir or not dest_dir:
        return

    # User Input
    chapters_input = simpledialog.askstring("Input", "Enter Chapter (e.g., '10.5-12' or '3'):")
    if not chapters_input:
        return

    folder_list = []

    try:
        if "-" in chapters_input:
            parts = [p.strip() for p in chapters_input.split("-")]
            start_val = float(parts[0])
            end_val = float(parts[1])

            low = min(start_val, end_val)
            high = max(start_val, end_val)

            # 1. Add the starting chapter
            folder_list.append("CH{0:g}".format(low))

            # 2. Add all whole-numbered chapters between the terminals
            # Find the first integer strictly greater than the low terminal
            current_int = int(math.floor(low) + 1)
            while current_int < high:
                folder_list.append("CH" + str(current_int))
                current_int += 1

            # 3. Add the ending chapter if it is distinct from the start
            if high != low:
                folder_list.append("CH{0:g}".format(high))
        else:
            # Single chapter input
            val = float(chapters_input.strip())
            folder_list = ["CH{0:g}".format(val)]

    except ValueError:
        messagebox.showerror("Error", "Invalid input format. Use numbers only.")
        return

    results = []

    # Process Folder Migration
    for folder_name in folder_list:
        src_path = os.path.join(source_dir, folder_name)
        dst_path = os.path.join(dest_dir, folder_name)

        if os.path.exists(src_path):
            try:
                if not os.path.exists(dst_path):
                    shutil.copytree(src_path, dst_path)
                    results.append("Copied: " + folder_name)
                else:
                    results.append("Skipped: " + folder_name + " (Already exists in destination)")
            except Exception as e:
                results.append("Error: " + folder_name + " (" + str(e) + ")")
        else:
            results.append("Not Found: " + folder_name)

    # Output Final Summary
    messagebox.showinfo("Migration Report", "\n".join(results))


if __name__ == "__main__":
    run_module_5()