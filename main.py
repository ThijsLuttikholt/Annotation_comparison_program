####### Import Libraries #######
import pdfkit
from jinja2 import Environment, FileSystemLoader
import os
import SimpleITK as sitk
import numpy as np

from utils.Frames import FOLDER_NAME, PDF_NAME, FRAMES, OCT_FILE, MY_FILE, RICK_FILE
from utils.get_images import getImages

def makePdf(pdfname, images):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("Annotation_template.html")

    html_string = template.render({})

    html_string = editHtmlString(html_string, images)

    path_wkhtmltopdf = os.getcwd().replace("\\","/")+"/wkhtmltopdf/bin/wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'enable-local-file-access': None,
        'no-outline': None
    }


    print('\n------------ Converting HTML to PDF -------------')
    pdfkit.from_string(html_string
                    , pdfname
                    , configuration=config
                    , options = options)

#Note that in the below, the MTC in the names means that the strings are already fit for other elements to immediately follow them. 
#The imageNames variable will be a list of image paths
def editHtmlString(html_string, imageList):
    dummyHeading = "<div class='pagebreak'><h2>Dummy for style </h2> <h1>Dummy header</h1></div><br>\n\n    "
    
    replaceString = ""
    for i, frame in enumerate(FRAMES):
        replaceString = replaceString + dummyHeading.replace("Dummy header", f"Frame: {frame}")
        replaceString = editHtmlString_help(replaceString, imageList[i])
    
    new_html = html_string.replace("Dummy for adding images",replaceString)
    return new_html

def editHtmlString_help(replaceString, p2_images):
    dummyImMTC = "<figure class='line__figure figure'>\n        <img src='dummy_image_path' ; width='420px'; height='420px' >\n        <figcaption>Dummy for image labels</figcaption>\n    </figure>\n\n    "
    openFieldSet = "<fieldset class='p2'>"
    for i in range(len(p2_images)):
        if i%2 == 0 and i != 0:
            replaceString = replaceString + "</fieldset><fieldset class='p2'>"
        elif i==0:
            replaceString = replaceString + "<fieldset class='p2'>"
        imName = "'file:///" + f"{p2_images[i][0]}'"
        intermediate = dummyImMTC.replace("'dummy_image_path'",imName)
        replaceString = replaceString + intermediate.replace("Dummy for image labels",p2_images[i][1])
    return replaceString + "</fieldset>"


##### The main function for report creation #####    
def main(folder_name, pdfname):
    #First we make preparations for the images:
    folder_path = os.getcwd().replace("\\","/") + f"/Annotations/{folder_name}/"
    my_image = sitk.ReadImage(folder_path+MY_FILE)
    my_array = sitk.GetArrayFromImage(my_image)

    rick_image = sitk.ReadImage(folder_path+RICK_FILE)
    rick_array = sitk.GetArrayFromImage(rick_image)

    oct_image = sitk.ReadImage(folder_path+OCT_FILE)
    oct_array = sitk.GetArrayFromImage(oct_image)

    myFrames = np.copy(FRAMES)-1
    images = getImages(my_array,rick_array,oct_array, myFrames, folder_path)

    makePdf(pdfname, images)

if __name__ == "__main__":
    main(FOLDER_NAME, PDF_NAME)