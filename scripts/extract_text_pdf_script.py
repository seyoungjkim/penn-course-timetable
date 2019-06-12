from scripts.pdf_parser import extract_text_to_file
import os

PDF_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../pdf/"
TEXT_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/../raw-text/"

if __name__ == '__main__':
    for filename in os.listdir(PDF_DIRECTORY):
        print("Starting to extract text from " + filename)
        extract_text_to_file(
            PDF_DIRECTORY + filename,
            TEXT_DIRECTORY + filename[:3] + "-text.txt",
        )
