from docx.oxml import OxmlElement, ns
from PIL import Image, ImageOps


def get_subdocument(document, parents_node):
    doc = document
    for elt in parents_node:
        if ('l' in elt) and ('c' in elt):
            doc = doc.tables[-1].rows[elt['l']].cells[elt['c']]
    return doc


def add_border(input_image, output_image, border):
    img = Image.open(input_image)
    if isinstance(border, int) or isinstance(border, tuple):
        bimg = ImageOps.expand(img, border=border, fill='black')
    else:
        raise RuntimeError('Border is not an image or tuple')
    bimg.save(output_image)


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


def add_picture(document, path="", caption="", width=None, border=0, caption_switch=True):
    tmp_path = path
    if border > 0:
        splitted = tmp_path.split('/')
        final_path = '/'.join(splitted[:-1]) + '/tmp_' + splitted[-1]
        add_border(tmp_path, final_path, border)
        tmp_path = final_path

    if document.paragraphs[-1].text != '':
        run = document.add_paragraph('').add_run()
    else:
        run = document.paragraphs[-1].add_run()
    run.add_picture(tmp_path, width=width)
    if caption_switch:
        add_caption(document, 'Figure', caption)
    return None


def apply_legacy_style(elt, styles):
    for opt in styles:
        try:
            getattr(elt, opt['style'])
            setattr(elt, opt['style'], True)
        except:
            pass
