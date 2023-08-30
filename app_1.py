from flask import Flask, send_from_directory, redirect # Redirect put in function's return to send user to diff URL
from flask import request, render_template, abort, jsonify, make_response, send_file, flash, redirect, url_for
import werkzeug
from werkzeug.utils import secure_filename
import os
from io import BytesIO

from PyPDF2 import PdfWriter, PdfReader
from PyPDF2 import generic
from pdf2jpg import pdf2jpg
from PIL import Image
from pytesseract import pytesseract
import enum
import cv2
import numpy as np
import pandas as pd
from pypdf import PdfReader as pdfreads
import sys
import csv
import numpy
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import codecs

from tqdm import tqdm
from time import sleep

#%%

app = Flask(__name__)

filestore = []
allowed_extensions = {'pdf'}
app.config['UPLOAD_FOLDER'] = r"C:\Users\alistair.blair\OneDrive - BYCN\Desktop\Web App\Upload_Folder"
file_loc = [0]
app.config['MAX_CONTENT_LENGTH'] = 150 * 1024 * 1024  # 150 MB
selection = [0,0,0] # Index[0] = ocr, Index[1] = text, Index[2] = both
All_Data_Names = ["Drawing Title", "Drawing Number", "Issue Status", "Creation Date", "Revision", "Paper Size", "Scale", "Page"]
boxes = [0,0,0,0,0,0,0,0] # Index order follows 'All_Data_Names'
OCR_CSV_Output = os.path.join(app.config['UPLOAD_FOLDER'], "OCR_data_table.csv")
Read_CSV_Output = os.path.join(app.config['UPLOAD_FOLDER'], "Read_data_table.csv")
Master_CSV_Output = os.path.join(app.config['UPLOAD_FOLDER'], "Combined_data_table.csv")

######
@app.route('/', methods=['GET', 'POST'])
def home():
    # return render_template('master.html', selection=selection)
    return render_template('login_page.html', selection=selection)

# @app.route('/return', methods=['POST'])
# def ret_home():
#     return render_template('master.html', selection=selection)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            # return redirect(url_for('home'))
    # return render_template('login_page.html', error=error, selection=selection)
            return render_template('master.html', error=error, selection=selection)
            # return main()
            # return redirect(url_for('main'))
    return render_template('login_page.html', error=error, selection=selection)
#####

# @app.route('/main', methods=['GET', 'POST'])
# def main():
#     return render_template('master.html', selection=selection)




# @app.route('/', methods=['GET', 'POST'])
# def home():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             # return redirect(url_for('home'))
#             return render_template('login_page.html', error=error, selection=selection)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             return redirect(url_for('home'))
#     return render_template('login_page.html', error=error, selection=selection)






# @app.route('/upload_seejpg', methods=['POST'])
# def seejpg():
#     initpage = pdf2jpg.convert_pdf2jpg(file_loc[0], app.config['UPLOAD_FOLDER'], dpi=100, pages="1")
#     return render_template('master.html', error=error, selection=selection, initpage=initpage)







def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/downloads', methods=['POST'])
def selects():
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Here, save the file
            path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path_to_file)
            file_loc[0] = path_to_file
            
    #         return render_template('show_pdf.html')
    #         return render_template('master.html', selection=selection)
    #         # return''
    #     else:
    #         return 'That file type is not supported, must choose PDF'
        
    # return 'No file uploaded'
    ocr = request.form.get('Method1', "0")
    text = request.form.get('Method2', "0")
    
    if ocr == "OCR":
        selection[0] = 1
    if ocr == "0":
        selection[0] = 0
    if text == "Text":
        selection[1] = 1
    if text == "0":
        selection[1] = 0
    if ocr == "OCR" and text == "Text":
        selection[2] = 1
    else:
        selection[2] = 0

    # return render_template('data_choice.html', selection=selection)

    drawtit = request.form.get('Data1', "0")
    drawnumb = request.form.get('Data2', "0")
    issstat = request.form.get('Data3', "0")
    creatdat = request.form.get('Data4', "0")
    revs = request.form.get('Data5', "0")
    papsiz = request.form.get('Data6', "0")
    scal = request.form.get('Data7', "0")
    pag3 = request.form.get('Data8', "0")
    
    if drawtit == "Drawing Title":
        boxes[0] = 1
    if drawtit == "0":
        boxes[0] = 0
    if drawnumb == "Drawing Number":
        boxes[1] = 1
    if drawnumb == "0":
        boxes[1] = 0
    if issstat == "Issue Status":
        boxes[2] = 1
    if issstat == "0":
        boxes[2] = 0
    if creatdat == "Creation Date":
        boxes[3] = 1
    if creatdat == "0":
        boxes[3] = 0
    if revs == "Revision":
        boxes[4] = 1
    if revs == "0":
        boxes[4] = 0
    if papsiz == "Paper Size":
        boxes[5] = 1
    if papsiz == "0":
        boxes[5] = 0
    if scal == "Scale":
        boxes[6] = 1
    if scal == "0":
        boxes[6] = 0
    if pag3 == "Page":
        boxes[7] = 1
    if pag3 == "0":
        boxes[7] = 0
    
    # return render_template('final.html', selection=selection)

# Naming output, can rename as desired

# @app.route('/preview', methods=['POST'])

# @app.route('/final', methods=['POST'])
# def generate_data():  
    Chosen_Names = []
    for i in range(len(boxes)):
        if boxes[i] == 1:
            Chosen_Names.append(All_Data_Names[i])
    
    # Converting from list to str for ease
    your_pdf = file_loc[0]
    Free_Folder = app.config['UPLOAD_FOLDER']
    
    # Check dimension size of pdf
    reader = pdfreads(your_pdf)
    box = reader.pages[0].mediabox
    print("PDF Dimensions: ", box)
    
    # Define Functions to aid pdf crop
    
    def ordinary_crop(x0, y0, x1, y1): # Coordinates that indicate the part of pdf that will remain
        scale_fac = box[2]/2384  # Scaling factor of 1 represents pdf of size ([0, 0, 2384, 1684])
        region = [x0, y0, x1, y1]
        scaled_crop = list(np.uint32(region)*scale_fac)  # turn into numpy array, apply scale, then returns as list
        return scaled_crop
    
    def counter_90_crop(x0, y0, x1, y1):
        transformer = [1, 0, 3, 2]  # Coordinate Transformation for 90 degree rotation
        scale_fac = box[3]/2384
        region = [2384-x0, y0, 2384-x1, y1]  # 2384 to account for inverse direction of x axis progression (2384 is used in defining standard pdf)
        scaled_crop = [list(np.uint32(region)*scale_fac)[i] for i in transformer]
        return scaled_crop

    #OCR

    # Cropping PDFs
    if selection[0] == 1 or selection[2] == 1:
        if box[2]<box[3]: # Accounting for 90 degree rotation anti-clockwise. A coordinate transformation of x1 -> -y1, y1 -> x1
            Drawing_Title = generic.RectangleObject(counter_90_crop(1640, 55, 1950, 145))
            Drawing_No_Box = generic.RectangleObject(counter_90_crop(2050, 150, 2325, 185))
            Issue_Status = generic.RectangleObject(counter_90_crop(2015, 100, 2150, 132))
            Creation_Date = generic.RectangleObject(counter_90_crop(2155, 100, 2260, 132))
            Revision = generic.RectangleObject(counter_90_crop(2280, 105, 2325, 132))
            Paper_Size = generic.RectangleObject(counter_90_crop(2075, 58, 2125, 85))
            Scale = generic.RectangleObject(counter_90_crop(2170, 58, 2260, 85))
            Page = generic.RectangleObject(counter_90_crop(2280, 58, 2325, 90))
        
        else:
            Drawing_Title = generic.RectangleObject(ordinary_crop(1640, 55, 1950, 145))
            Drawing_No_Box = generic.RectangleObject(ordinary_crop(2050, 150, 2325, 185))
            Issue_Status = generic.RectangleObject(ordinary_crop(2015, 100, 2150, 132))
            Creation_Date = generic.RectangleObject(ordinary_crop(2155, 100, 2260, 132))
            Revision = generic.RectangleObject(ordinary_crop(2280, 105, 2325, 132))
            Paper_Size = generic.RectangleObject(ordinary_crop(2075, 58, 2125, 85))
            Scale = generic.RectangleObject(ordinary_crop(2170, 58, 2260, 85))
            Page = generic.RectangleObject(ordinary_crop(2280, 58, 2325, 90))
        #####
        
        All_Data = [Drawing_Title, Drawing_No_Box, Issue_Status, Creation_Date, Revision, Paper_Size, Scale, Page]
        All = []
    
        for i in range(len(boxes)):
            if boxes[i] == 1:
                All.append(All_Data[i])
        #####
        
        with open(your_pdf, "rb") as in_f:
            input1 = PdfReader(in_f)
            output = PdfWriter()
        
            numPages = len(input1.pages)
            print("document has %s pages." % numPages)
        
            for i in range(0, len(All)):
        
                for j in range(numPages):
                    page = input1.pages[j]
                    page.cropbox = All[i]
                    output.add_page(page)
        
                with open(os.path.join(Free_Folder, "Cropped_%s.pdf" % All[i]), "wb") as out_f:
                    output.write(out_f)
        
        # PDF to JPEGs
        result = pdf2jpg.convert_pdf2jpg(os.path.join(Free_Folder, "Cropped_%s.pdf" % All[len(All)-1]), Free_Folder, dpi=100, pages="ALL")
    
        # PyTesseract as OCR (Optical Character Recognition)
        tess_exec_0 = os.path.join(os.getcwd(), "Tesseract_Folder")
        tess_exec = os.path.join(tess_exec_0, "tesseract.exe")
        tesseract_exe = tess_exec # Converting from Tkinter obj to str for ease
        
        class OS(enum.Enum):
            Windows = 1
        
        class Language(enum.Enum):
            ENG = 'eng'
        
        class ImageReader:
            def __init__(self, os: OS):
                if os == OS.Windows:
                    windows_path = tesseract_exe
                    pytesseract.tesseract_cmd = windows_path
            def extract_text(self, image: str, lang: str) -> str:
                img = Image.open(image)
                extracted_text = pytesseract.image_to_string(img, lang=lang)
                return extracted_text
        
        # To Run tesseract.exe
        ir = ImageReader(OS.Windows)
        
        # Conversion to Greyscale used, doesn't work properly without
        arr = [] # Array of all the texts made
        n0_of_jpegs = numPages*(len(All))
        for i in range(0, n0_of_jpegs):
            image = cv2.imread(os.path.join(Free_Folder, "Cropped_%s.pdf_dir\%s_Cropped_%s.pdf.jpg" % (All[len(All)-1], i, All[len(All)-1])))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
            thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            if __name__ == '__main__':
                if i < numPages:
                    data = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
                    processed_text = ' '.join(data.split())
                    # Removed_White_Space = processed_text.replace(" ","")
                    print(processed_text)
                    arr.append(processed_text)
                else:
                    data = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
                    processed_text = ' '.join(data.split())
                    Removed_White_Space = processed_text.replace(" ", "")
                    print(Removed_White_Space)
                    arr.append(Removed_White_Space)
        
        # Generating Pandas DataFrame for the data
        datapoints = []
        for i in range(len(All)):
            if i == 0:
                arrays = arr[0:numPages]
                datapoints.append(arrays)
            else:
                arrays = arr[numPages*i:numPages*(i+1)]
                datapoints.append(arrays)
        
        transposed = np.transpose(datapoints)
        d0 = pd.DataFrame(np.array(transposed), columns=Chosen_Names)
        
        # Downloading DataFrame Table as Excel CSV
        d0.to_csv(OCR_CSV_Output)
    
        # Remove generated files (keeping only csv data file)
        for i in range(0, len(All)):
            os.remove(os.path.join(Free_Folder, "Cropped_%s.pdf" % All[i]))
        
        for i in range(0, n0_of_jpegs):
            os.remove(os.path.join(Free_Folder, "Cropped_%s.pdf_dir\%s_Cropped_%s.pdf.jpg" % (All[len(All)-1], i, All[len(All)-1])))
        
        directory = 'Cropped_%s.pdf_dir' % (All[len(All)-1])
        path = os.path.join(Free_Folder, directory)
        os.rmdir(path)
    
    """
    Above is Reading the Data via OCR Method (for if data in PDF is picture based)
    
    Below is Reading the Data by Read Method - Reading the text or the annotations
    (for if data in PDF is written based)
    """
    
    # Cell for obtaining data from pdf by Reading text
    
    if selection[1] == 1 or selection[2] == 1:
        reader = PdfReader(your_pdf) 
        writer = PdfWriter()
        
        csv_file = open(Read_CSV_Output, 'w', newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        
        csv_writer.writerow(['PDF Page #'] + Chosen_Names)
        print('this file has ', len(reader.pages), " pages")
        #for page in reader.pages:
        for page_id, page in enumerate(reader.pages):
        
            page_size_x = float(page.cropbox[2])
            page_size_y = float(page.cropbox[3])
            
            print("x:", page_size_x,"y:", page_size_y)
            
            block_corners =  {'x_min': 0.6536, 'y_min': 1-0.8843, 'x_max': 0.9840, 'y_max': 1-0.9658}
            title_corners =  {'x_min': 0.6536, 'y_min': 1-0.9138, 'x_max': 0.8443, 'y_max': 1-0.9663}
            dwgnum_corners = {'x_min': 0.8438, 'y_min': 1-0.8903, 'x_max': 0.9838, 'y_max': 1-0.9110}
            issue_stat = {'x_min': 0.845218, 'y_max': 0.059382, 'x_max': 0.901846, 'y_min': 0.0783848} #
            create_dat = {'x_min': 0.9039429, 'y_max': 0.059382, 'x_max': 0.9479866, 'y_min': 0.0783848}#
            degrev_corners = {'x_min': 0.9538, 'y_min': 1-0.9218, 'x_max': 0.9840, 'y_max': 1-0.9388}
            pap_size = {'x_min': 0.8703859, 'y_max': 0.0344418052, 'x_max': 0.89135906, 'y_min': 0.05047506}#
            scal = {'x_min': 0.910234899, 'y_max': 0.0344418052, 'x_max': 0.9479865772, 'y_min': 0.05047506}#
            pag_num = {'x_min': 0.9563758389, 'y_max': 0.0344418052, 'x_max': 0.9752516779, 'y_min': 0.05344418052}#
            
            if page_size_x >= page_size_y: #check if it is horizontal
                page.cropbox.upper_left  = (page_size_x*block_corners['x_min'], page_size_y*block_corners['y_min'])
                page.cropbox.lower_right = (page_size_x*block_corners['x_max'], page_size_y*block_corners['y_max'])
                
            writer.add_page(page) 
        
            drawing_title = []#
            drawing_title_y = []#
            drawing_number = []#
            
            drawing_stat = []#
            drawing_date = []#
            
            drawing_revision = []#
            
            drawing_pap = []#
            drawing_scal = []#
            drawing_pagnum = []#
            
            def visitor_body(text, cm, tm, fontDict, fontSize):
        
                 
                y = tm[5]/page_size_y
                x = tm[4]/page_size_x
        
                if page_size_x >= page_size_y: #check if it is horizontal
                    if   y > title_corners['y_max'] and y < title_corners['y_min'] and x > title_corners['x_min'] and x < title_corners['x_max'] :   
                        drawing_title.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                        drawing_title_y.append(y)
        
                    elif y > dwgnum_corners['y_max'] and y < dwgnum_corners['y_min'] and x > dwgnum_corners['x_min'] and x < dwgnum_corners['x_max'] :
                        drawing_number.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                    
                    elif y > issue_stat['y_max'] and y < issue_stat['y_min'] and x > issue_stat['x_min'] and x < issue_stat['x_max'] :
                        drawing_stat.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                    
                    elif y > create_dat['y_max'] and y < create_dat['y_min'] and x > create_dat['x_min'] and x < create_dat['x_max'] :
                        drawing_date.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
        
                    elif y > degrev_corners['y_max'] and y < degrev_corners['y_min'] and x > degrev_corners['x_min'] and x < degrev_corners['x_max'] :
                        drawing_revision.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                    
                    elif y > pap_size['y_max'] and y < pap_size['y_min'] and x > pap_size['x_min'] and x < pap_size['x_max'] :
                        drawing_pap.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                    
                    elif y > scal['y_max'] and y < scal['y_min'] and x > scal['x_min'] and x < scal['x_max'] :
                        drawing_scal.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                    
                    elif y > pag_num['y_max'] and y < pag_num['y_min'] and x > pag_num['x_min'] and x < pag_num['x_max'] :
                        drawing_pagnum.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                    
                    
                else: #check if it is vertical
                    if   y > (1-title_corners['x_max']) and y < (1-title_corners['x_min']) and x > title_corners['y_max'] and x < title_corners['y_min'] :   
                        drawing_title.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                        drawing_title_y.append(y)
        
                    elif y > (1-dwgnum_corners['x_max']) and y < (1-dwgnum_corners['x_min']) and x > dwgnum_corners['y_max'] and x < dwgnum_corners['y_min'] :
                        drawing_number.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                    
                    elif y > (1-issue_stat['x_max']) and y < (1-issue_stat['x_min']) and x > issue_stat['y_max'] and x < issue_stat['y_min'] :
                        drawing_stat.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                    
                    elif y > (1-create_dat['x_max']) and y < (1-create_dat['x_min']) and x > create_dat['y_max'] and x < create_dat['y_min'] :
                        drawing_date.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
        
                    elif y > (1-degrev_corners['x_max']) and y < (1-degrev_corners['x_min']) and x > degrev_corners['y_max'] and x < degrev_corners['y_min'] :
                        drawing_revision.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                    
                    elif y > (1-pap_size['x_max']) and y < (1-pap_size['x_min']) and x > pap_size['y_max'] and x < pap_size['y_min'] :
                        drawing_pap.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                    
                    elif y > (1-scal['x_max']) and y < (1-scal['x_min']) and x > scal['y_max'] and x < scal['y_min'] :
                        drawing_scal.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                    
                    elif y > (1-pag_num['x_max']) and y < (1-pag_num['x_min']) and x > pag_num['y_max'] and x < pag_num['y_min'] :
                        drawing_pagnum.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                    
            page.extract_text(visitor_text = visitor_body)
            
            if "/Annots" in page:
                for annot in page["/Annots"]:
                    obj = annot.get_object()
                    annotation = {
                        "location0": obj["/Rect"],
                        "content": obj["/Contents"]
                    }
                    #print(annotation)
                    x = (obj["/Rect"][0]+obj["/Rect"][2])/(2*page_size_x)
                    y = (obj["/Rect"][1]+obj["/Rect"][3])/(2*page_size_y)
                    text = obj["/Contents"]
                    if page_size_x >= page_size_y: #check if it is horizontal
                        if   y > title_corners['y_max'] and y < title_corners['y_min'] and x > title_corners['x_min'] and x < title_corners['x_max'] :   
                            drawing_title.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                            drawing_title_y.append(y)
        
                        elif y > dwgnum_corners['y_max'] and y < dwgnum_corners['y_min'] and x > dwgnum_corners['x_min'] and x < dwgnum_corners['x_max'] :
                            drawing_number.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                        
                        elif y > issue_stat['y_max'] and y < issue_stat['y_min'] and x > issue_stat['x_min'] and x < issue_stat['x_max'] :
                            drawing_stat.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                        
                        elif y > create_dat['y_max'] and y < create_dat['y_min'] and x > create_dat['x_min'] and x < create_dat['x_max'] :
                            drawing_date.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
        
                        elif y > degrev_corners['y_max'] and y < degrev_corners['y_min'] and x > degrev_corners['x_min'] and x < degrev_corners['x_max'] :
                            drawing_revision.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                        
                        elif y > pap_size['y_max'] and y < pap_size['y_min'] and x > pap_size['x_min'] and x < pap_size['x_max'] :
                            drawing_pap.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                        
                        elif y > scal['y_max'] and y < scal['y_min'] and x > scal['x_min'] and x < scal['x_max'] :
                            drawing_scal.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                        
                        elif y > pag_num['y_max'] and y < pag_num['y_min'] and x > pag_num['x_min'] and x < pag_num['x_max'] :
                            drawing_pagnum.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                        
                    else: #check if it is vertical
                        if   y > (1-title_corners['x_max']) and y < (1-title_corners['x_min']) and x > title_corners['y_max'] and x < title_corners['y_min'] :   
                            drawing_title.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                            drawing_title_y.append(y)
        
                        elif y > (1-dwgnum_corners['x_max']) and y < (1-dwgnum_corners['x_min']) and x > dwgnum_corners['y_max'] and x < dwgnum_corners['y_min'] :
                            drawing_number.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                        
                        elif y > (1-issue_stat['x_max']) and y < (1-issue_stat['x_min']) and x > issue_stat['y_max'] and x < issue_stat['y_min'] :
                            drawing_stat.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                        
                        elif y > (1-create_dat['x_max']) and y < (1-create_dat['x_min']) and x > create_dat['y_max'] and x < create_dat['y_min'] :
                            drawing_date.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
        
                        elif y > (1-degrev_corners['x_max']) and y < (1-degrev_corners['y_max']) and x > degrev_corners['y_max'] and x < degrev_corners['y_min'] :
                            drawing_revision.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                        
                        elif y > (1-pap_size['x_max']) and y < (1-pap_size['x_min']) and x > pap_size['y_max'] and x < pap_size['y_min'] :
                            drawing_pap.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                        
                        elif y > (1-scal['x_max']) and y < (1-scal['x_min']) and x > scal['y_max'] and x < scal['y_min'] :
                            drawing_scal.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
                        
                        elif y > (1-pag_num['x_max']) and y < (1-pag_num['x_min']) and x > pag_num['y_max'] and x < pag_num['y_min'] :
                            drawing_pagnum.append(text.replace('\n', ' ').strip().replace('DRAWING TITLE', ''))
        
            text_drawing_title    = ' '.join(filter(None, list(x for _, x in sorted(zip(drawing_title_y, drawing_title), reverse=True))))
            text_drawing_number   = ' '.join(filter(None, drawing_number))
            text_drawing_stat   = ' '.join(filter(None, drawing_stat))
            text_drawing_date   = ' '.join(filter(None, drawing_date))
            text_drawing_revision = ' '.join(filter(None, drawing_revision))
            text_drawing_pap   = ' '.join(filter(None, drawing_pap))
            text_drawing_scal   = ' '.join(filter(None, drawing_scal))
            text_drawing_pagnum   = ' '.join(filter(None, drawing_pagnum))
            
            tot_list = [text_drawing_title, text_drawing_number, text_drawing_stat, text_drawing_date, text_drawing_revision,
                       text_drawing_pap, text_drawing_scal, text_drawing_pagnum]
    
            current_list = []
            for i in range(len(boxes)):
                if boxes[i] == 1:
                    current_list.append(tot_list[i])
            # print(current_list)
    
        #    print(text_body)
            to_write = [page_id+1]
            for i in range(len(current_list)):
                to_write.append(current_list[i])
                
                
                
            print(to_write)
            csv_writer.writerow(to_write)
            
        #    break
    
        csv_file.close()
    
    # This combined both data from OCR and Reading into once CSV file to compare
    
    def Convert(lst):
       res_dct = map(lambda i: (lst[i], lst[i+1]), range(len(lst)-1)[::2])
       return dict(res_dct)
    
    if selection[2] == 1:
        d1 = pd.read_csv(Read_CSV_Output)
        new_frame_data_list = []
        for i in range(len(Chosen_Names)):
            new_frame_data_list.append(Chosen_Names[i] + '(from read)')
            new_frame_data_list.append(d1['%s' % Chosen_Names[i]].values.tolist())
            new_frame_data_list.append(Chosen_Names[i] + '(from OCR)')
            new_frame_data_list.append(d0['%s' % Chosen_Names[i]].values.tolist())
    
        new_dict = Convert(new_frame_data_list)
        combined_df = pd.DataFrame(new_dict)
        combined_df.to_csv(Master_CSV_Output)

    return render_template('master2.html', selection=selection)

@app.errorhandler(413)
def too_large(placehold):
    return make_response(jsonify(message="File is too large: 150 MB is the set limit"), 413)

@app.route('/download', methods=['POST'])
def download():
    if selection[0] == 1:
        filenamer = OCR_CSV_Output
        return send_file(filenamer, as_attachment=True)
    else:
        return "OCR wasn't selected earlier in the process"

@app.route('/download1', methods=['POST'])
def download1():
    if selection[1] == 1:
        filenamer = Read_CSV_Output
        return send_file(filenamer, as_attachment=True)
    else:
        return "Text Read wasn't selected earlier in the process"

@app.route('/download2', methods=['POST'])
def download2():
    if selection[2] == 1:
        filenamer = Master_CSV_Output
        return send_file(filenamer, as_attachment=True)
    else:
        return "Both OCR and Text Read wasn't selected earlier in the process"



# @app.route('/table', methods=['POST'])
# def data():
#     # if selection[0] == 1:
#     #     with open("%s" % OCR_CSV_Output) as file:
#     #         reader = csv.reader(file)
#     #         return render_template("table1.html", csv=reader)
#     # else:
#     #     return "No Preview Available"
#     table = pd.read_csv('%s' % Read_CSV_Output, encoding= 'unicode_escape')
#     return render_template("table1.html", data=table.to_html())

@app.route('/dataframe', methods=['POST'])
def dataframe():
    df = pd.read_csv('%s' % OCR_CSV_Output, encoding= 'unicode_escape')
    return render_template('table1.html', tables=[df.to_html(classes='data', header="true")])

@app.route('/dataframe1', methods=['POST'])
def dataframe1():
    df1 = pd.read_csv('%s' % Read_CSV_Output, encoding= 'unicode_escape')
    return render_template('table2.html', tables=[df1.to_html(classes='data', header="true")])

@app.route('/dataframe2', methods=['POST'])
def dataframe2():
    df2 = pd.read_csv('%s' % Master_CSV_Output, encoding= 'unicode_escape')
    return render_template('table3.html', tables=[df2.to_html(classes='data', header="true")])
    
    
    

@app.route('/delete', methods=['POST'])
def delete_data():
    if selection[0] == 1:
        os.remove(OCR_CSV_Output)
    if selection[1] == 1:
        os.remove(Read_CSV_Output)
    if selection[2] == 1:
        os.remove(Master_CSV_Output)
    os.remove(file_loc[0])
    # return redirect(url_for('selects'))
    # return render_template('master2.html', selection=selection)
    # return redirect('/download')
    # return "Your data has been removed from the servers."
    return render_template('master3.html')

if __name__ == "__main__":
    app.run(host="localhost", port = 8890, debug=True) # localhost == 127.0.0.1 --> this is the local host, thus points to your own computer
    
# Make it so that the user can draw on the pdf to indicate what data from what area they want
    
    
