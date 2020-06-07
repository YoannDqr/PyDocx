from tags import *
from styles import *


def inheritance(inheritance):
    for elt in inheritance:
        for i in range(0, len(elt)-1):
            STYLE_FUNCTIONS[elt[i]] = STYLE_FUNCTIONS[elt[-1]]


def gen_alias(tag, options=None, classes=None, styles=None):
    if options is None:
        options = {}
    if classes is None:
        classes = []
    if styles is None:
        styles = {}
    alias = tag
    for key, value in options.items():
        alias += SPLIT_OPTION + key + SPLIT_OPTION_VALUE + SPACE_CHAR.join(value.split(' '))
    for key, value in styles.items():
        alias += SPLIT_CLASS + key + SPLIT_STYLE_VALUE + SPACE_CHAR.join(value.split(' '))
    for elt in classes:
        alias += SPLIT_CLASS + elt
    return alias, tag


# Special characters used by the language
TAG_CHAR = '£$'
TAG_CHAR_END = '$£'
SPLIT_OPTION = ':'
SPLIT_CLASS = '?'
SPLIT_STYLE_PROPS = '?'
SPLIT_STYLE_VALUE = '='
SPLIT_STYLE = ':'
SPLIT_OPTION_VALUE = '='
SPLIT_CELLS = '|'

SPACE_CHAR = '_'

# Links tags name to their functions
TAGS_FUNCTIONS = {
    'title': title,
    'img': img,
    'p': p,
    'sstring': styled_string,
    'table': table,
    'nmap': nmap,
    'ssl': testssl,
    'part': stall,
}

# Links tag name to their style functions
# Use of lambda function allows more flexibility
STYLE_FUNCTIONS = {
    'img': {
        'align': lambda document, value: paragraph_align(document.paragraphs[-2:], value),
        'caption': lambda document, value: caption_style(document.paragraphs[-1], value)
    },
    'p': {
        'align': lambda document, value: paragraph_align(document.paragraphs[-1], value),
        'style': lambda document, value: global_paragraph_style(document.paragraphs[-1], value),
        'size': lambda document, value: paragraph_font_size(document.paragraphs[-1], value),
        'color': lambda document, value: paragraph_font_color(document.paragraphs[-1], value),
        'indent': lambda document, value: paragraph_indentation(document.paragraphs[-1], value)
    },
    'table': {
        'style': lambda document, value: global_table_style(document.tables[-1], value),
        'cellColor': lambda document, value: cells_background_color(document.tables[-1], value),
        'align': lambda document, value: paragraph_align(document.paragraphs[-1], value),
        'cellAlign': lambda document, value: cells_alignement(document.tables[-1], value),
        'caption': lambda document, value: caption_style(document.paragraphs[-1], value),
        'indent': lambda document, value: table_indentation(document.tables[-1], value),
        'autofit': lambda document, value: set_autofit(document.tables[-1], value),
        'merge': lambda document, value: merge(document.tables[-1], value)
    },
}

inheritance([
    ('nmap', 'ssl', 'table'),
])

# Create alias for tags.
# When the template will be read, the dict key will be replaced by the value.
# It is useful to create custom tags and snippets

ALIAS = {
    'li': gen_alias('p', styles={'style': 'List Bullet'}),
    'code': gen_alias('p', styles={'style': 'Code'}),
    'b': gen_alias('sstring', options={'run_bold': '1'}),
    'i': gen_alias('sstring', options={'run_italic': '1'}),
    'table': gen_alias('table', options={'delimiter': SPLIT_CELLS}, styles={
        'style': 'Tableau Solucom',
        'indent': '0',
        'caption': 'TitreFigure2'
    }),
    'img': gen_alias('img', options={'border': '5'}),
    'nmap': gen_alias('nmap', styles={
        'style': 'Tableau Solucom',
        'indent': '0',
        'cellAlign': '*/*#CENTER',
        'autofit': '1',
        'align': 'CENTER',
        'caption': 'TitreFigure2'
    }),
    'ssl': gen_alias('ssl', styles={
        'style': 'Tableau Solucom',
        'indent': '0',
        'cellAlign': '*/*-0#CENTER!*/0#LEFT',
        'autofit': '1',
        'align': 'CENTER',
        'caption': 'TitreFigure2'
    }),
}


