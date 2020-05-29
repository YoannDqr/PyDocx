from docx import Document
from settings import *
from tools import get_subdocument


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
                index = i+1
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


def generate_graph(line, parent=None):
    if parent is None:
        parent = []
    result = []
    index = line.find(split_char)
    while index != -1:
        option_end = line.find(' ', index)
        tmp = line.find('\n', index)
        if tmp < option_end and tmp != -1:
            option_end = tmp

        option, classes, styles = process_option(line[index+len(split_char): option_end])

        end_index = line.find(split_char+option['name'], index+1)

        new_parent = parent + [option]
        node_header = {'option': option, 'class': classes, 'style':styles}
        if index == 0 or parent == []:
            result += [[node_header] + generate_graph(line[option_end+1:end_index-1], parent=new_parent)]
        else:
            result += [line[:index]] + [[node_header] + generate_graph(line[option_end + 1:end_index - 1], parent=new_parent)]

        if end_index + len(split_char) + len(option['name']) < len(line):
            line = line[end_index+len(split_char)+len(option['name']):]
        else:
            line = ''
        index = line.find(split_char)

    if line != '':
        result += [line]
    return result


def apply_global_style(document, classe, gstyle, inline_style):
    option_name = classe[-1]
    for elt in classe:
        if elt in gstyle:
            for key, value in gstyle[elt].items():
                if not(key in inline_style):
                    try:
                        style_functions[option_name][key](document, value)
                    except:
                        print("[W] - Style proprety `{}={}` is not implemented for element `{}`".format(key, value, option_name))

    for key, value in inline_style.items():
        try:
            style_functions[option_name][key](document, value)
        except:
            print("[W] - Style proprety `{}={}` is not implemented for element `{}`".format(key, value, option_name))


def graph2doc(document, graph, current, gstyle=None, parents_node=None):
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

            tags_functions[option['name']](subdoc, option, elt, parents_node+[option])
            apply_global_style(subdoc, classes+[option['name']], gstyle, styles)

        elif type(elt) == list:
            apply_global_style(subdoc, classes + [option['name']], gstyle, styles)
            graph2doc(subdoc, elt, current, gstyle=gstyle, parents_node=parents_node+[option])


def process_aliases(data):
    for key, value in alias.items():
        if key in data:
            first = False
            splitted = data.split(split_char + key)
            data = ""
            for i in range(len(splitted)):
                if i == 0:
                    data = splitted[0]
                    first = not first
                else:
                    data += split_char+value[first]+splitted[i]
                first = not first
    return data


def initial_parsing(initial_data):
    data = ""
    style = {}
    keep_style = False
    for elt in initial_data:
        if elt != '\n':
            if split_char+'style' in elt:
                keep_style = not keep_style
                continue
            if keep_style:
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
    return style, data + split_char + "p " + split_char + "p"


doc = Document('docx/template.docx')
file = open("template.dqr", encoding="utf-8")
data = file.readlines()
style, data = initial_parsing(data)

graph_data = generate_graph(data)
for elt in graph_data:
    graph2doc(doc, elt, None, gstyle=style)

doc.save('docx/demo.docx')


