from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from tools import create_paragraph_style


def global_paragraph_style(paragraph, value):
    paragraph.style = value


def image_caption(paragraph, value):
    if paragraph.text != '':
        paragraph.style = value


def paragraph_font_size(paragraph, value):
    new_style = create_paragraph_style(paragraph)
    new_style.font.size = Pt(int(value))
    paragraph.style = new_style


def global_table_style(table, value):
    table.style = value


def paragraph_align(paragraph, value):
    if type(paragraph) != list:
        paragraphs = [paragraph]
    else:
        paragraphs = paragraph
    for elt in paragraphs:
        elt.alignment = WD_ALIGN_PARAGRAPH.__dict__[value]
