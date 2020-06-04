from tags import *
from styles import *


def inheritance(inheritance):
    for elt in inheritance:
        for i in range(0, len(elt)-1):
            style_functions[elt[i]] = style_functions[elt[-1]]


def gen_alias(tag, options=None, classes=None, styles=None):
    if options is None:
        options = {}
    if classes is None:
        classes = []
    if styles is None:
        styles = {}
    alias = tag
    for key, value in options.items():
        alias += split_options + key + split_options_value + option_space_char.join(value.split(' '))
    for key, value in styles.items():
        alias += split_class + key + split_style_value + option_space_char.join(value.split(' '))
    for elt in classes:
        alias += split_class + elt
    return alias, tag


# Special characters used by the language
split_char = '£$'
split_char_end = '$£'
split_options = ':'
split_class = '?'
split_style_props = '?'
split_style_value = '='
split_style = ':'
split_options_value = '='
split_cells = '|'

option_space_char = '_'

# Links tags name to their functions
tags_functions = {
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
style_functions = {
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

alias = {
    'li': gen_alias('p', styles={'style': 'List Bullet'}),
    'code': gen_alias('p', styles={'style': 'Code'}),
    'b': gen_alias('sstring', options={'run_bold': '1'}),
    'i': gen_alias('sstring', options={'run_italic': '1'}),
    'table': gen_alias('table', options={'delimiter': split_cells}, styles={
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

constraints_tags = [
    'test'
]

constraints_schem = {
    'test': ['intro', 'test', 'conclusion']
}


