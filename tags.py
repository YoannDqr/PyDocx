from docx.shared import Cm
from docx.table import _Cell
from tools import *


def title(document, option, value, parents_node, preprocessing=False):
    if preprocessing:
        return None
    current = document.add_heading(value, int(option['rank']))
    return current


def img(document, option, value, parents_node, preprocessing=False):
    if preprocessing:
        return None

    if not('path' in option):
        return None
    try:
        border = int(option['border'])
    except:
        border = 0
    try:
        width = Cm(int(option['width']))
    except:
        width = None
    caption = not('caption' in option)

    add_picture(
        document,
        path=option['path'],
        caption=value,
        width=width,
        border=border,
        caption_switch=caption
    )


def styled_string(document, option, value, parents_node, preprocessing=False):
    if preprocessing:
        return None

    added = document.paragraphs[-1].add_run(value)
    apply_legacy_style(added, parents_node)


def p(document, option, value, parents_node, preprocessing=False):
    if preprocessing:
        if type(document) == _Cell and document.paragraphs[-1].text == "":
            document.paragraphs[-1]
        else:
            document.add_paragraph('')

    else:
        document.paragraphs[-1].add_run(value)


def table(document, option, value, parents_node, preprocessing=False):
    if preprocessing:
        if ('c' in option) and ('l' in option):
            document.add_table(rows=int(option['l']), cols=int(option['c']))
            if 'caption' in option:
                add_caption(document, 'Table', option['caption'])
            option['c'], option['l'] = 0, 0
    else:
        split_cells = option['delimiter']
        elt = value.strip()
        if elt == split_cells:
            option['c'] += 1

        if option['c'] == len(document.tables[-1].rows[0].cells) - 1 and not (elt == split_cells):
            option['l'] += 1
            option['c'] = 0


