import subprocess
import os


def pdf2txt(
    in_pdf_path: str,
    out_txt_path: str
) -> str:
    """Convert pdf to text file

    Examples:
        >>> pdf2txt(
        >>>    in_pdf_path='../data/sample/7203/7203.pdf',
        >>>    out_txt_path='./7203.txt'
        >>> )
    """
    EDITABLE_TMP_FILE_PATH = in_pdf_path.replace('.pdf', '_editable.pdf')
    # OUT_TXT_PATH = in_pdf_path.replace('.pdf', '.txt')

    MK_PDF_EDITABLE_CMD = 'pdftk'
    PDF_TO_TEXT_CMD = 'pdftotext'

    try:
        # make pdf editable
        subprocess.call([
            MK_PDF_EDITABLE_CMD,
            in_pdf_path,
            'output',
            EDITABLE_TMP_FILE_PATH
        ])

        # convert pdf to text
        subprocess.call([
            PDF_TO_TEXT_CMD,
            EDITABLE_TMP_FILE_PATH,
            out_txt_path
        ])
    finally:
        if os.path.exists(EDITABLE_TMP_FILE_PATH):
            os.remove(EDITABLE_TMP_FILE_PATH)

    return out_txt_path
