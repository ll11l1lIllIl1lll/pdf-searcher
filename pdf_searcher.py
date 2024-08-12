import os
import argparse
import PyPDF2
from tqdm import tqdm

def search_text_in_pdf(pdf_path, text):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                if text in page.extract_text():
                    return True
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return False

def search_in_directory(directory, text):
    pdf_files = []
    all_files = []

    # Gather all PDF files first for better progress tracking
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                all_files.append(os.path.join(root, file))

    # Use tqdm to show progress
    for pdf_path in tqdm(all_files, desc="Searching PDFs", unit="file"):
        if search_text_in_pdf(pdf_path, text):
            pdf_files.append(pdf_path)

    return pdf_files

def main():
    parser = argparse.ArgumentParser(description="Search for text in all PDF files in a directory.")
    parser.add_argument('directory', help="Directory to search for PDF files.")
    parser.add_argument('text', help="Text to search for in the PDF files.")

    args = parser.parse_args()

    matching_files = search_in_directory(args.directory, args.text)

    if matching_files:
        print("The following PDF files contain the specified text:")
        for file in matching_files:
            print(file)
    else:
        print("No PDF files contain the specified text.")

if __name__ == "__main__":
    main()