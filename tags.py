def title(document, option, value):
    if 'title' in option['name']:
        current = document.add_heading(value, int(option['name'].split('title')[1]))
    return current