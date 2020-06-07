# PyDocx
This python script was developed to speed up Word document
writing. Thus, the script will compile a markup text file
into a readable and handsome Word document.
The whole markup language can be customized to meet your needs.
Indeed, it is possible to quickly modify every tag, the syntax
as well as implement new tags depending on your needs.
The major asset is to be able to define python routine that can
easily generate a fancy word document for few lines of codes.
For example, generating table from data stored in a file, automatically
applied the same style to many Word elements as set up image borders, 
captions, etc. 
# Table of content
1. [Built-in tags](#builtintags)
    1. [Titles](#title)
    2. [Paragraphs](#p)
        1. [Tag and options](#p-tags)
        2. [Alias and shortcuts](#p-alias)
    3. [Styled Strings](#sstring)
        1. [Tag and options](#sstring-tags)
        2. [Alias and shortcuts](#sstring-alias)
    4. [Images](#img)
    5. [Tables](#tbl)
2. [Structure of the project](#structure)
    1. [Abstract syntax tree](#AST)
    2. [tags.py](#tags_file)
    3. [styles.py](#styles_file)
    4. [settings.py](#settings_file)
        1. [Tags customization](#tags_custo)
        2. [Styles customization](#style_custo)
        3. [Alias](#alias)
        4. [Tags inheritance](#inheritance)
        5. [Syntax customization](#syntax_custo)
    5. [Global style and classes](#global_style)
3. [VsCode extension](#vscode)
## Built-in tags <a name="builtintags"></a>
### Titles <a name="title"></a>
___
Titles can be generated using the tag `title`. The option `rank` can be 
used to modify the level of the title.
For example, the following code will generate title of levels 1 to 3:
```
£$title:rank=1 Title 1 $£title
£$title:rank=2 Title 2 $£title
£$title:rank=3 Title 3 $£title
```
### Paragraphs <a name="p"></a>
___
Paragraphs are the basic element for Word document. Indeed, every piece
of text written in a Word document belongs to a paragraph. 
Thus, every text written must belong to a paragraph.
#### Tag and options <a name="p-tags"></a>
The tag for paragraph is `p`. Thus, the following code will generate
a single word paragraph :
```dqr
£$p This text belongs to a paragraph $£p
```
Without any other options, Word will apply the `Normal` style to
this paragraph. For the moment, the following style properties are
implemented :
- `align` : Alignment of the paragraph. Values can be `RIGHT`, `LEFT`, `CENTER`
`DISTRIBUTE`, `JUSTIFY_HI`, `JUSTIFY_MED`, `JUSTIFY_LOW`. A complete explanation
of these values can be found [here](https://docs.microsoft.com/en-us/office/vba/api/Word.WdParagraphAlignment).
- `style` : Complete style of the paragraph. Sometimes it's easier to directly
define and set up named style in Word. The value of this style property is the 
name of the style as defined in Word. For example, bullet lists are paragraph
with a special style.
- `size` : Font size. The value is the size of the font.
- `color` : Font color. The value is the hexadecimal value of the color.
- `indent` : Indentation of the paragraph. The value is the size of the indentation.
The following code will generate a paragraph aligned to the left, with a font
size of 13, a special color, and an custom indentation value :
```dqr 
£$p?align=LEFT?size=13?color=#eaeaea?indent=5 
    This paragraph is customized !
$£p
```
The following code will generate a bullet list using the Word built-in style :
```dqr
£$p?style=List_Bullet element 1 $£p
£$p?style=List_Bullet element 2 $£p
£$p?style=List_Bullet element 3 $£p
```
#### Alias and Shortcut <a name="p-alias"></a>
Some shortcuts/alias are already defined :
- `li` : `p?style=List_Bullet` will generate a bullet list item.
- `code` : `p?style=Code` will generate a code paragraph
Thus, the following code will generate a bullet list :
```
£$li element 1 $£li
£$li element 2 $£li
£$li element 3 $£li
```
### Styled strings <a name="sstring"></a>
___
#### Tag and options <a name="sstring-tags"></a>
Styled strings are tags, noted `sstring`, are used to apply a special style to a part
of a paragraph.
For example, make some words in bold or italic.
The following code will create a paragraph with some words in bold
and others is italic:
```dqr
£$p
 This is plaintext, 
 £$sstyle:run_bold=1 but this is bold text $£sstyle 
 £$sstyle:run_italic=1 and this is italic text $£sstyle
$£p
```
#### Alias and shortcuts <a name="sstring-alias"></a>
Some shortcut/alias are already defined :
- `b` : `sstring:run_bold=1` will generate a bold text
- `i` : `sstring:run_italic=1` will generate an italic text.
### Images <a name="img"></a>
___
This tag is used to integrate images in the document. The image
will be added in a brand new paragraph.
Moreover, this tag allows to add a caption to the image with an
automatic Word caption numbering.
The following code will integrate an image to the document :
```
£$img:path=dir/img.png Caption for the figure $£img
```
Some options are already defined for this tag :
- `path` : this option is the relative or absolute path to the image
- `border` : this option, if present, will add a border to the image. 
The value of this option is the width of the border.
- `width` : this option, if present, will modify the width of the image.
The height will be proportionately adjusted. The value if the width in `cm`
- `caption` : this option, if present, will delete the caption of the figure.
Moreover, some styles properties are also implemented:
- `align` : this style give the alignment of the image and its caption.
The value expected is the same than those for paragraph alignment
- `caption` : this style allows to set a special Word style to the caption.
The value is the name of a Word style.
The following code will generate an image, with a border, center aligned,
with a width of 7cm and a caption with a custom style :
```
£$img:path=img.jpg:border=5:width=7?align=CENTER?caption=TitreFigure2 Caption of the figure $£img
```
 
### Tables <a name="tbl"></a>
___
Tables are generated with the tag `table`. Two options are mandatory : the option 
`l` and the option `c`. These options are used to indicate the number of lines
and columns of the table. Then, the character `|` is used to split cells.
A new line is represented by a carriage return. 
The content of each cell must be a tag. Thus, a cell can be a simple paragraph,
an image or another table.
Thus, the following code will generate a table of two lines and three columns.
One of the cells will be filled with an image.
```dqr
£$table:l=2:c=3
    £$p cell1 $£p | £$p cell2 £$p | £$p cell3 £$p
    £$p cell4 £$p | £$p cell5 £$p | £$img:path=image.jpg:caption=0 $£img
$£
```
Several options are already implemented :
- `style`: global style of the table. The value must be the name of the table
style as defined in Word.
- `caption`: optional caption for the table. The value is the content of the caption.
- `align`: alignment of the table caption. The value is the same than these defined
for paragraph alignment.
- `indent`: indentation to apply to all cells. The value is the size of the indentation.
- `autofit`: set column width auto-fit. If this option is present, thus, the column
width will be modified to fit the content.
- `merge`: merge cells. The value of this property will be explained in the next paragraph.
- `cellAlign`: alignement of cells. The value of this property will be explained in the next paragraph.
- `cellColor`: color of the cell. The value of this property will be explained in 
the next paragraph.
The `cellAlign` and `cellColor` properties are special because they
can be applied to specific cells. To target these cell, a special syntax must be followed.
The syntax is as follow:
```dqr
row1-row2-...-rown/col1-col2-...-colm#value
```
Thus, the property will be applied to each cell such as its row and column is
listed.
For example, the following code `1-2/1#CENTER` will apply the value
`CENTER` for the cells with coordinate (1, 1) and (2, 1).
Is it possible to chain these syntax. Thus, the code :
```
1-2/1#CENTER!1-2/2-3#JUSTIFY
```
will center cells whose coordinates are (1, 1) or (1, 2), and justify cells
whose coordinates are (1, 2), (1, 3), (2, 2) or (2, 3).
Sometimes, it's easier to apply the style to all rows or columns except some.
This can be done using the character `*`. If this character is present in
the row or column list, thus, every row or columns will be selected except
these listed.
For example, the following code `*-1/*#CENTER` will center all cells except
the first row.
The syntax is the same for the three properties `cellAlign`, `cellColor`.

The `merge` property accept as value the following syntax :
```dqr
row-col/row1-col1
```
This will merge all columns between the cell (row, col) et the cell (row1, col1).
The following example shows the use of the merge property to merge all cell of the 
same row for a table with 4 columns:
```dqr
£$table:merge=1-1/1-4 ... $£table
```
## Structure of the project <a name="structure"></a>
### Abstract syntax tree <a name="AST"></a>
To generate the word document, the user must write a text file 
following a syntax he can totally customize. The syntax is based
on tags. A tag is just a keyword preceded by a special symbol.
For this document, the special symbol will be `£$` for tag opening
and `$£` for tag ending.
An example of text file could be
```dqr
#Code Example 1
£$title:rank=1 This is a title 1 $£
    £$title:rank=2 This is a title 2 $£ 
    £$p 
        This is a paragraph
        £$b This is bold text $£
    $£p
    £$table:l=2:c=3:caption=Table_caption?style=Table_Style
        $£p cell1 $£p | $£p cell2 $£p | $£p cell3 £$b with bold text $£b $£p
        $£p cell4 $£p | $£p cell5 $£p | $£p cell6 £$b with bold text $£b $£p
    $£table
```
This text document will be used to generate the abstract language tree (AST).
In the AST, nodes are tag's name, option, style and class. 
To explain these notions, the line corresponding to the table definition
used in the `Code example 1` will be taken as an example.
- The name of the tag is the value of the tag, so here `table`
- The options of the tag are values which will affect the design
of the element once translated in Word document. In the example,
options are separated with the special character `:`. They are
l, c, and caption. l defined the number of lines, c the number of columns
and caption the content of the table caption.
- The style of the tag is the Word style that shall be applied to the element.
For example, the style with keyword `style` will apply the Word table style named
`Table Style`. Style properties are separated with the special character `?`
- The class of a tag is similar to html element class. It allows to
apply the same style to all tags with the same class. This will be
seen later.
Thus the each node of the AST will be composed of these four values.
Tree leaves will be raw text.
For the example of the table defined in `Code example 1`, the AST will be :
___
![AST](./readme/AST_example.jpg)
___
When this tree is generated, it will be traversed following his
infix course.
As said at the beginning, the whole syntax of the text file can 
be customized. Then, special character used before every tag, 
character used to split option, style and classes, as well as
the definition or redefinition of tags can be modified.
Literally everything can be modified.
To make it easier, the project is split in different files :
### tags.py <a name="tags_file"></a>
___
This file compiles python functions related to a tag.
For example, if a paragraph is defined by the tag `£$p`,
thus, a corresponding function need to be defined in the
file `tags.py` in order to handle the `£$p` tag.
Every function dedicated to tag handling must follow the
same prototype : `def function(document, option, value, parents_node, preprocessing=False)`
 with :
 - `document` : this variable represents the current element 
 in the Word document. For example, if the function handle a
 paragraph, the `document` parameter will represent the current
 Word paragraph
 - `option` : this parameter is the list of options given to the
 tag. Options are defined by the user when he writes his tag.
 - `value` : this is the content written between the opening tag
 and the closing tag. For example, in the following code : `£$p salut les copains $£p`
 `value` will be equal to `salut les copains`.
 - `parents_node` : this parameter is the list of all parents tag and their options
 of the current tag. For example, with the following code `£$p £$b salut £$b $£p`,
 the variable `parents_node` will be empty for the tag `£$p` and will equal to `£$p`
 for the tag `£$b`
 - `preprocessing` : this boolean parameter allows to perform actions before the content
 of the tag is evaluated and processed. The following image show
 where the code defined in the preprocessing part will be applied
 during the tree parsing.
 ___
 ![Preprocessing](readme/preprocessing.jpg)
 ___
 
 The following code is an example of function defining the tag
 `p` used to generate a Word paragraph:
 ```python
def p(document, option, value, parents_node, preprocessing=False):
    if preprocessing:
        if type(document) != _Cell or document.paragraphs[-1].text != "":
            document.add_paragraph('')
    else:
        document.paragraphs[-1].add_run(value)
 ```
Here, the preprocessing flag is used to generate the new paragraph,
then, once the paragraph is created, the function will be used to add
the value to the brand new paragraph.
### styles.py <a name="styles_file"></a>
___
Functions defined in this file will handle style of element whatever
it is inline style or style defined by classes.
As for tags function, style functions must follow the same 
prototype : `def function(document_elt, value)` where :
- `document_elt` is the element whose style must be applied
- `value` is the value of the style. For example, if the style
function is used to align paragraph, the value can be RIGHT, LEFT
, CENTER etc...
The following code is an example of style function allowing to
modify the alignment of a paragraph:
```python
def paragraph_align(paragraph, value):
    if type(paragraph) != list:
        paragraphs = [paragraph]
    else:
        paragraphs = paragraph
    for elt in paragraphs:
        elt.alignment = WD_ALIGN_PARAGRAPH.__dict__[value]
```
 
 ### settings.py <a name="settings_file"></a>
 ___
 This file is used to map all functions defined in tags.py, style.py
 and the tag name.
 
 #### Tags customization <a name="tags_custo"></a>
 The mapping done between the tag name and his function is done
 in the dictionary `tags_function`.
 For example, the following code :
 ```python
tags_function = {
    'p': tags_function_for_paragraph
}
 ``` 
This code maps the `tags_function_for_paragraph` to the tag `p`.
#### Styles customization <a name="style_custo"></a>
Style's properties are mapped with the `style_functions` dictionary.
This dictionary is defined as follows:
```python
style_functions = {
    'p': {
        align = lambda document, value: paragraph_align(document.paragraphs[-1], value)  
    },
}
```
#### Alias <a name="alias"></a>
Alias are tags writing shortcut. For example, if you know that all
image of your document must follow the same style or options, it is
possible to define alias.
For example, if all images must be bordered it is possible to 
define the following alias :
```dqr
img <=> img:border=5
```
Alias are defined in the dictionary `alias`. To make easier the
definition of alias, the function `gen_alias` can be used.
The following code is used to define alias :
```dqr
alias = {
    'img': gen_alias('img', options={'border': '5'}, style={}, classes=[]),
}
```
#### Tags inheritance <a name="inheritance"></a>
Sometime new tags will be defined, but styles that can be applied to this
new tag are the same than the one applied for another tag.
To avoid repeating every definition of the style for this new tag,
it is possible to simply define an inheritance link between these
two tags.
For example, the tag `filetable` is a tag that will generate a table
from data stored in a file. This tag is not the `table` tag but in
Word document it will be materialized in the same way : a table. Thus,
every style of `table` tag can also be applied to `filetable` tag.
The inheritance link can be done with the following code :
```python
inheritance([
    ('filetable', 'other_tag_looking_like_table', 'table'),
])
```
 
#### Syntax customization <a name="syntax_custo"></a>
 Moreover, it is in this file that every constant used can be 
 customized :
 ```dqr
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
 ```
### Global style and classes <a name="global_style"></a>
It is possible to define global style in the text file using the tag `style`.
These style can be applied to all character sharing the same name or the same class.
For example, the following code :
```dqr
£$style
    fancy_img:align=CENTER?caption=Intense Quote
    p:align=LEFT
$£style
£$img:path=...?fancy_img image caption $£img
£$p This is a paragraph $£p
£$imgpath=... image caption $£img
```
With this code, only the first image will be centered because it
has the class `fancy_img`.
However, every paragraph defined by the tag `p` will be aligned to the left.
 
## VsCode extension <a name="vscode"></a>
To make easier the writing of text file, an extension for Visual Studio Code is 
supplied.
The extension is in the folder `dqrlanguage` and can be added to the
directory `.vscode`.
The extension provides syntax highlighting, some code snippet etc...
However, the visual extension is not linked to the `settings.py` file, thus,
if any change is made in the file, the changes must also be referred 
in all files of the extension.