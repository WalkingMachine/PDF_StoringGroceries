#!/usr/bin/env python

from pylatex import Figure, PageStyle, Head, LineBreak, simple_page_number
from pylatex import Document, Section, Subsection, NoEscape, utils, LongTabu, StandAloneGraphic
import os
import datetime
import sys


def fill_document(doc, try_number):

    """Add a section, a subsection and some text to the document.

    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    cupboard_init_filename = os.path.join(os.path.dirname(__file__), 'objects/cupboard_init.png')

    header = PageStyle("header")

    # Create center header
    with header.create(Head("C")):
        header.append(LineBreak())
        header.append(utils.bold('Storing Groceries - PDF Report'))
        header.append(LineBreak())
        header.append("Try number: " + str(try_number))
    # Create right header
    with header.create(Head("R")):
        header.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    with header.create(Head("L")):
        header.append("Team name: Walking Machine")

    doc.preamble.append(header)
    doc.change_document_style("header")

    with doc.create(Figure(position='h!')) as cupboard_pic:
        cupboard_pic.add_image(cupboard_init_filename, width='120px')
        cupboard_pic.add_caption('Cupboard picture - initial state')
        cupboard_pic.add_image(cupboard_init_filename, width='120px')
        cupboard_pic.add_caption('Cupboard picture - final state')

    # Number of objects
    number_objects = len([name for name in os.listdir('objects') if os.path.isfile(os.getcwd()+"/objects/"+name)])

    # Add cheque images
    with doc.create(LongTabu("X[c] X[c]")) as cheque_table:
        for i in range(1, 4):
            cheque_table.add_row([StandAloneGraphic(os.path.join(os.path.dirname(__file__),
                                   'object'+str(i)+'.jpg'), image_options="width=200px"),
                                  StandAloneGraphic(os.path.join(os.path.dirname(__file__),
                                   'object'+str(8-i)+'.jpg'), image_options="width=200px")])

if __name__ == '__main__':
    # Basic document
    geometry_options = {"margin": "0.7in"}
    if len(sys.argv) > 1:
        try_number = int(sys.argv[1])
    else:
        try_number = 1
    doc = Document('WalkingMachine_'+str(try_number), geometry_options=geometry_options)
    fill_document(doc, try_number)
    doc.generate_pdf(clean_tex=False)




