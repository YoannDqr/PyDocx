from tags import *
from styles import *

# Special characters used by the language
split_char = '£$'
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
    },
    'table': {
        'style': lambda document, value: global_table_style(document.tables[-1], value)
    }
}

# Create alias for tags.
# When the template will be read, the dict key will be replaced by the value.
# It is useful to create custom tags and snippets
alias = {
    'li': ('p'+split_class+'style'+split_style_value+'List_Bullet', 'p'),
    'code': ('p'+split_class+'style'+split_style_value+'Code', 'p'),
    'b': ('sstring'+split_options+'style'+split_options_value+'bold', 'sstring'),
    '_i': ('sstring'+split_options+'style'+split_options_value+'italic', 'sstring'),
    'table': ('table'+split_class+'style'+split_style_value+'Tableau_Solucom'+split_options+'delimiter'+split_options_value+split_cells, 'table'),
    'img': ('img'+split_options+'border'+split_options_value+'5', 'img')
}


