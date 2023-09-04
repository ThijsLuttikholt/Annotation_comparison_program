### How to use this project: 

Using this project is fairly simple. There are 3 basic things you need to do: 
1) Download the wkhtmltopdf folder. This is used to change the html to a pdf.  https://wkhtmltopdf.org/downloads.html   Make sure to place the wkhtmltopdf folder in this project. At the same level as the annotations or utils folders. 
2) In the Annotations folder, create a folder (for example called Week_1)
3) In the Frames.py file, change the FOLDER_NAME variable to the name of the folder you created. 
4) In the same file, change the frame numbers to the ones you see in Excel for that week (no need to start from 0, the program does that itself)
5) Also in the Frames.py file, change the name of the report to what you want it to be. (don't forget the file extension)
6) Make sure the following files are present in the folder you created (with the file names I mention): 
- oct.dcm         This is the original oct image
- rick.nii.gz     This is Rick's annotation with which we want to compare.
- mine.nii.gz     This is your own annotation    

Make sure the file names are the same as above. If you want different file names. Change the corresponding names in the Frames.py file

Lastly, just run the main.py file. 

### Folder structure Annotations folder: 

The Annotations folder will contain separate folders for each week of annotation.    
In each separate folder, the program will automatically create an images folder.    
Make sure to remove the images once you no longer need them. 

### Interpretation of the overlay colors in the top-right image of the pdf: 
- Red: Any errors outside the other categories. 
- Green: I overestimated intima on the inside.
- Light green: I underestimated intima on the inside. 
- Blue: I underestimated the media (either inside or outside)
- Light blue: I overestimated the media (either inside or outside. )


### Required python libraries: 
- pdfkit     (pip install pdfkit)
- jinja2      (pip install Jinja2)
- os          
- SimpleITK   (pip install SimpleITK)
- numpy       (pip install numpy)
