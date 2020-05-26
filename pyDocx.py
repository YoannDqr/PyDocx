from docx import Document
from docx.shared import Cm
from docx.oxml import OxmlElement, ns
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image, ImageOps

split_char = '£$'
split_options = ':'
split_class = '?'
split_style_props = '?'
split_style_value = '='

# Set of functions used to apply styles.
# style_function[balise][option](document, value)
style_functions = {
    'img': {
        'align': lambda document, value: paragraph_align(document.paragraphs[-2:], value),
        'captionStyle': lambda document, value: global_paragraph_style(document.paragraphs[-1], value)
    },
    'p': {
        'align': lambda document, value: paragraph_align(document.paragraphs[-1], value),
        'style': lambda document, value: global_paragraph_style(document.paragraphs[-1], value)
    },
}


def add_xref(paragraph, type):
    run = paragraph.add_run()
    r = run._r
    fldChar = OxmlElement('w:fldChar')
    fldChar.set(ns.qn('w:fldCharType'), 'begin')
    r.append(fldChar)
    instrText = OxmlElement('w:instrText')
    instrText.text = ' SEQ '+type+' \* ARABIC'
    r.append(instrText)
    fldChar = OxmlElement('w:fldChar')
    fldChar.set(ns.qn('w:fldCharType'), 'end')
    r.append(fldChar)


def add_caption(document, type, caption):
    paragraph = document.add_paragraph(type, style='Caption')
    add_xref(paragraph, type)
    paragraph.add_run(': ' + caption)
    return paragraph


def process_option(option):
    try:
        options, classes = option.split(split_class)
    except ValueError:
        options = option
        classes = ""
    option_args = options.split(split_options)
    result = {'name': option_args[0]}
    for i in range(0, len(option_args)//2):
        result[option_args[2*i+1]] = option_args[2*(i+1)]

    return result, classes


def add_picture(document, path="", caption="", width=None, border=0):
    tmp_path = path
    if border > 0:
        add_border(tmp_path, 'tmp_'+tmp_path, 5)
        tmp_path = 'tmp_' + tmp_path

    document.add_picture(tmp_path, width=width)
    current = add_caption(document, 'Figure', caption)
    return current


def add_border(input_image, output_image, border):
    img = Image.open(input_image)
    if isinstance(border, int) or isinstance(border, tuple):
        bimg = ImageOps.expand(img, border=border, fill='black')
    else:
        raise RuntimeError('Border is not an image or tuple')
    bimg.save(output_image)


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
        option, classes = process_option(line[index+len(split_char): option_end])
        end_index = line.find(split_char+option['name'], index+1)

        new_parent = parent + [option]
        node_header = {'option': option, 'class': classes}
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


def apply_paragraph_style(elt, styles):
    for opt in styles:
        if opt['name'] == "b":
            elt.bold = True
        elif opt['name'] == "i":
            elt.italic = True


def global_paragraph_style(paragraph, value):
    paragraph.style = value


def paragraph_align(paragraph, value):
    if type(paragraph) != list:
        paragraphs = [paragraph]
    else:
        paragraphs = paragraph
    for elt in paragraphs:
        elt.alignment = WD_ALIGN_PARAGRAPH.__dict__[value]


def apply_global_style(document, classe, style):
    classe_list = classe.split(split_class)
    option_name = classe_list[-1]
    for elt in classe_list:
        if elt in style:
            for stl in style[elt].split(split_style_props):
                key, value = stl.split(split_style_value)
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
    styles = list(parents_node)
    if option['name'] == 'p':
        current = document.add_paragraph('')
    if option['name'] == 'li':
        current = document.add_paragraph(style='List Bullet')
    styles += [option]

    for elt in graph[1:]:
        if type(elt) == str:
            if 'title' in option['name']:
                current = document.add_heading(elt, int(option['name'].split('title')[1]))
            elif 'img' in option['name'] and 'path' in option:
                try:
                    border = int(option['border'])
                except:
                    border = 0
                try:
                    width = Cm(int(option['width']))
                except:
                    width = None
                current = add_picture(
                    document,
                    path=option['path'],
                    caption=elt,
                    width=width,
                    border=border
                )
            else:
                added = current.add_run(elt)
                apply_paragraph_style(added, styles)

            apply_global_style(document, classes+split_class+option['name'], gstyle)

        elif type(elt) == list:
            graph2doc(document, elt, current, gstyle=gstyle, parents_node=styles)


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
                key, value = elt.split(':')
                style[key.strip()] = value.strip()
            else:
                data += elt.lstrip()
    return style, data+split_char+"p "+split_char+"p"


doc = Document()
file = open("template.dqr", encoding="utf-8")
data = file.readlines()
style, data = initial_parsing(data)

graph_data = generate_graph(data)

print(style)
print(graph_data)
for elt in graph_data:
    graph2doc(doc, elt, None, gstyle=style)

doc.save('demo.docx')


