# Import Necessary packages
from docx import Document
from docx.shared import Inches


def MakeDocument(statement):
    document = Document()
    document.add_heading(statement)
    firstStatement = document.add_paragraph("Does this work??")
    document.add_page_break()
    document.save("Tryout.docx")
