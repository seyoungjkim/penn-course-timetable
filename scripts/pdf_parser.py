from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from io import StringIO


# Returns text from pdf in string format
def extract_text(pdf_path):
    output = StringIO()
    resource_manager = PDFResourceManager()
    device = TextConverter(resource_manager, outfp=output)
    page_interpreter = PDFPageInterpreter(resource_manager, device)
    with open(pdf_path, 'rb') as fp:
        for page in PDFPage.get_pages(fp, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        page_text = output.getvalue()
    device.close()
    output.close()
    return page_text


def extract_text_to_file(pdf_path, txt_path):
    page_text = extract_text(pdf_path)
    with open(txt_path, "w+") as file:
        file.write(page_text)
