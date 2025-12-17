import os
from PIL import Image


def get_sort_number(filename):
    name_only = filename.lower().replace('.psd', '')
    num_str = "".join([char for char in name_only if char.isdigit()])
    return int(num_str) if num_str else filename


def image_generator(folder, files):
    """
    Opens, converts, and yields one image at a time to save memory.
    """
    for filename in files:
        path = os.path.join(folder, filename)
        try:
            # We use 'with' to ensure the file handle is managed
            with Image.open(path) as img:
                print(f"Processing: {filename}")
                yield img.convert("RGB")
        except Exception as e:
            print(f"Error processing {filename}: {e}")


def module_06_psd_to_pdf_streaming(input_folder, output_filename):
    # 1. Get and sort files
    files = [f for f in os.listdir(input_folder) if f.lower().endswith('.psd')]
    try:
        files.sort(key=get_sort_number)
    except ValueError:
        files.sort()

    if not files:
        print("No PSD files found.")
        return

    # 2. Initialize the generator
    # We slice [1:] because the first image is handled by the save() call
    img_stream = image_generator(input_folder, files[1:])

    # 3. Open the first image to start the PDF
    first_path = os.path.join(input_folder, files[0])
    try:
        with Image.open(first_path) as first_img:
            base_img = first_img.convert("RGB")

            # 4. The 'save' function pulls from the generator one by one
            base_img.save(
                output_filename,
                "PDF",
                resolution=72.0,
                save_all=True,
                append_images=img_stream
            )
            print(f"\n✅ Streaming Complete! PDF saved: {output_filename}")

    except Exception as e:
        print(f"Failed to create PDF: {e}")


if __name__ == "__main__":
    # module_06_psd_to_pdf_streaming("./chapter_folder", "QA_Reference_72dpi.pdf")
    folder = input("Enter the folder containing PSD files: ")
    out_pdf = input("Enter the name of the output PDF file: ")
    module_06_psd_to_pdf_streaming(folder, out_pdf)
