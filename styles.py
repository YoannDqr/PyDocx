from docx.enum.text import WD_ALIGN_PARAGRAPH


def global_paragraph_style(paragraph, value):
    paragraph.style = value


def image_caption(paragraph, value):
    if paragraph.text != '':
        paragraph.style = value


def bold_paragraph(paragraph, value):
    paragraph.bold = bool(int(value))


def global_table_style(table, value):
    table.style = value


def paragraph_align(paragraph, value):
    if type(paragraph) != list:
        paragraphs = [paragraph]
    else:
        paragraphs = paragraph
    for elt in paragraphs:
        elt.alignment = WD_ALIGN_PARAGRAPH.__dict__[value]
