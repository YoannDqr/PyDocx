from docx import Document
from settings import *
from tools import get_subdocument, progress_bar


def generate_graph(line, parent=None):
    def process_option(option):
        option_args = []
        raw_classes = []
        result = (option_args, raw_classes)
        key = True
        index = 0
        first = True
        if split_class in option or split_options in option:
            for i in range(len(option)):
                if option[i] == split_class or option[i] == split_options:
                    if first:
                        tag_name = option[:i]
                        first = False
                    else:
                        result[key].append(option[index:i])
                    index = i + 1
                    key = option[i] == split_class

            result[key].append(option[index:])
        else:
            tag_name = option

        options = {'name': tag_name}
        styles = {}
        classes = []

        for elt in option_args:
            splitted = elt.split(split_options_value)
            if len(splitted) > 1:
                options[splitted[0]] = " ".join(splitted[1].split(option_space_char))

        for elt in raw_classes:
            splitted = elt.split(split_style_value)
            if len(splitted) == 2:
                styles[splitted[0]] = " ".join(splitted[1].split(option_space_char))
            else:
                classes.append(elt)

        return options, classes, styles

    if parent is None:
        parent = []
    result = []
    index = line.find(split_char)
    while index != -1:
        option_end = line.find(' ', index)
        tmp = line.find('\n', index)
        if tmp < option_end and tmp != -1:
            option_end = tmp

        option, classes, styles = process_option(line[index + len(split_char): option_end])

        end_index = line.find(split_char_end + option['name'], index + 1)
        subline = line[option_end + 1:end_index - 1]
        while subline.count(split_char+option['name']) != subline.count(split_char_end+option['name']):
            end_index = line.find(split_char_end + option['name'], index + 1 + end_index)
            subline = line[option_end + 1:end_index - 1]

        new_parent = parent + [option]
        node_header = {'option': option, 'class': classes, 'style': styles}
        if index == 0 or parent == []:
            result += [[node_header] + generate_graph(subline, parent=new_parent)]
        else:
            result += [line[:index]] + [
                [node_header] + generate_graph(subline, parent=new_parent)]

        if end_index + len(split_char) + len(option['name']) < len(line):
            line = line[end_index + len(split_char) + len(option['name']):]
        else:
            line = ''
        index = line.find(split_char)

    if line != '':
        result += [line]
    return result


def graph2doc(document, graph, current, gstyle=None, parents_node=None):
    def apply_global_style(document, classe, gstyle, inline_style):
        option_name = classe[-1]
        for elt in classe:
            if elt in gstyle:
                for key, value in gstyle[elt].items():
                    if not (key in inline_style):
                        try:
                            style_functions[option_name][key](document, value)
                        except KeyError:
                            print("[W] - Style property `{}={}` is not implemented for element `{}`".format(key, value,
                                                                                                            option_name))

        for key, value in inline_style.items():
            try:
                style_functions[option_name][key](document, value)
            except KeyError:
                print(
                    "[W] - Style property `{}={}` is not implemented for element `{}`".format(key, value, option_name))

    if parents_node is None:
        parents_node = []
    if gstyle is None:
        gstyle = {}

    option = graph[0]['option']
    classes = graph[0]['class']
    styles = graph[0]['style']

    subdoc = get_subdocument(document, parents_node)

    tags_functions[option['name']](subdoc, option, None, parents_node, preprocessing=True)
    for elt in graph[1:]:
        if type(elt) == str:

            tags_functions[option['name']](subdoc, option, elt, parents_node + [option])
            apply_global_style(subdoc, classes + [option['name']], gstyle, styles)

        elif type(elt) == list:
            apply_global_style(subdoc, classes + [option['name']], gstyle, styles)
            graph2doc(document, elt, current, gstyle=gstyle, parents_node=parents_node + [option])


def initial_parsing(initial_data):
    def process_aliases(data):
        for key, value in alias.items():
            data = data.replace(split_char+key, split_char+value[0])
            data = data.replace(split_char_end+key, split_char_end+value[1])

        return data

    data = ""
    style = {}
    keep_style = False
    for elt in initial_data:
        if elt != '\n':
            if split_char + 'style' in elt:
                keep_style = True
            elif split_char_end + 'style' in elt:
                keep_style = False
            elif keep_style:
                key, value = elt.split(split_style)
                for style_opt in value.strip().split(split_style_props):
                    prop, val = style_opt.split(split_style_value)
                    try:
                        style[key.strip()][prop] = val
                    except:
                        style[key.strip()] = {prop: val}
            else:
                data += elt.lstrip()
    data = process_aliases(data)
    return style, data + split_char + "p " + split_char_end + "p"


def doc_creation(doc, graph_data):
    maxi = len(graph_data)
    progress = 0
    for elt in graph_data:
        progress_bar(progress, maxi, title='Doc creation')
        graph2doc(doc, elt, None, gstyle=style)
        progress += 1
    progress_bar(progress, maxi, title='Doc creation')


doc = Document('docx/template.docx')
file = open("template2.dqr", encoding="utf-8")
data = file.readlines()

style, data = initial_parsing(data)
data = data
graph_data = generate_graph(data)
doc_creation(doc, graph_data)

i = 0
save = False
while save is not True:
    try:
        doc.save('docx/demo{}.docx'.format(i))
        print('Document generated in docx/demo{}.docx'.format(i))
        save = True
    except:
        i += 1
