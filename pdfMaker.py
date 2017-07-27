# -*- coding: utf-8 -*- 
#!/usr/bin/env python

from pylatex import Figure, PageStyle, Head, LineBreak, simple_page_number
from pylatex import Document, Section, Subsection, NoEscape, utils, LongTabu, StandAloneGraphic
import os
import datetime
import numpy
import getpass
from shutil import copyfile


import sys
reload(sys)
sys.setdefaultencoding("utf-8")




def fill_document(doc, try_number):

    """Add a section, a subsection and some text to the document.

    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """

    """ ~/roi_images_objects 
        scene.png
    """

    #cupboard_init_filename = os.path.join(os.path.dirname(__file__), 'objects/cupboard/cupboard_init.png')
    folder_path = '/home/'+getpass.getuser()
    cupboard_init_filename = folder_path + '/scene.png'


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
    if os.path.exists(folder_path + '/detection_1/'):
        with doc.create(Figure(position='h!')) as cupboard_pic:
            cupboard_pic.add_image(folder_path+'/detection_1/scene.png', width='120px')
            cupboard_pic.add_caption('Cupboard picture - initial state')
            if os.path.exists(folder_path + '/detection_3/'):
                cupboard_pic.add_image(folder_path + '/detection_3/scene.png', width='120px')
                cupboard_pic.add_caption('Cupboard picture - final state')

    if os.path.exists(folder_path+'/detection_2/'):
        # Number of objects
        #number_objects = len([name for name in os.listdir('objects') if os.path.isfile(os.getcwd()+"/objects/"+name)])
        liste_fichiers = [name for name in os.listdir(folder_path+'/detection_2/') if os.path.isfile(folder_path+'/detection_2/'+name) and name != 'scene.png' and name != 'scene2.png']
        print liste_fichiers
        # Add cheque images
        with doc.create(LongTabu("X[c] X[c]")) as image_table:
            nb_row = int(numpy.ceil(len(liste_fichiers) / 2.0))
            for i in range(1, nb_row+1):
                file1 = folder_path+'/'+liste_fichiers[i-1]
                if i == nb_row and len(liste_fichiers) < 2*nb_row:
                    file2 = ''
                else:
                    file2 = folder_path+'/'+liste_fichiers[(i-1+nb_row)]

                image_table.add_row([StandAloneGraphic(file1, image_options="width=200px"),
                                      StandAloneGraphic(file2, image_options="width=200px")])

if __name__ == '__main__':
    # Basic document
    geometry_options = {"margin": "0.7in"}
    if len(sys.argv) > 1:
        try_number = int(sys.argv[1])

    else:
        try_number = 1
    doc = Document('WalkingMachine_'+str(try_number), geometry_options=geometry_options)
    fill_document(doc, try_number)
    try:
        doc.generate_pdf(clean_tex=False)
    except:
        print "oups"
    src_path = '/home/' + getpass.getuser() +'/pdfMaker_Robocup/'+ 'WalkingMachine_'+str(try_number)+'.pdf'
    usb_path = '/media/'+getpass.getuser()+'/8919-DC72/WalkingMachine_'+str(try_number)+'.pdf'
    copyfile(src_path, usb_path)
