from tags import *
from styles import *

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
    'table': table
}

# Links tag name to their style functions
style_functions = {
    'img': {
        'align': lambda document, value: paragraph_align(document.paragraphs[-2:], value),
        'caption': lambda document, value: image_caption(document.paragraphs[-1], value)
    },
    'p': {
        'align': lambda document, value: paragraph_align(document.paragraphs[-1], value),
        'style': lambda document, value: global_paragraph_style(document.paragraphs[-1], value),
        'size': lambda document, value: paragraph_font_size(document.paragraphs[-1], value)
    },
    'table': {
        'style': lambda document, value: global_table_style(document.tables[-1], value)
    }
}


# Create alias for tags.
# When the template will be read, the dict key will be replaced by the value.
# It is useful to create custom tags and snippets


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


alias = {
    'li': gen_alias('p', styles={'style': 'List Bullet'}),
    'code': gen_alias('p', styles={'style': 'Code'}),
    'b': gen_alias('sstring', options={'run_bold': '1'}),
    '_i': gen_alias('sstring', options={'run_italic': '1'}),
    'table': gen_alias('table', options={'delimiter': split_cells}, styles={'style': 'Tableau Solucom'}),
    'img': gen_alias('img', options={'border': '5'})
}


