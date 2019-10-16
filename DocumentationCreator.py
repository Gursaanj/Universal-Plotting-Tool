# Import Necessary packages
from docx import Document
from docx.shared import Inches


def MakeDocument(statement):
    document = Document()
    document.add_heading(statement)
    firstStatement = document.add_paragraph("Does this work??")
    document.add_page_break()
    document.save("Tryout.docx")


# Ideas to add to documentation creator:
# Save image of plot
# save display trendLine data
# have the CBDV logo as a Watermark/Logo
# Markus' signature. credibility
# WISHLIST:: All corresponding error plot and analysis (in a simple to read table??)
