import numpy as np
import math

from PIL import Image as im
from PIL import ImageDraw, ImageFont
import scipy.ndimage as sim
import os

def getImages(my_array, rick_array, oct_array, frames, annFolder):
    imFolder = annFolder + "images/"
    if not os.path.exists(imFolder):
        os.makedirs(imFolder)
    all_images = []
    for frame in frames:
        page = getOnePage(my_array[frame],rick_array[frame],oct_array[frame], imFolder,frame)
        all_images.append(page)
    return all_images

def getOnePage(my_frame, rick_frame, oct_frame, imFolder, frame):
    #Some set-up:
    imName1 = imFolder + f"{frame}_oct.png"
    imName2 = imFolder + f"{frame}_difference.png"
    imName3 = imFolder + f"{frame}_rick.png"
    imName4 = imFolder + f"{frame}_mine.png"
    label1 = f"Frame {frame}: OCT image"
    label2 = f"Frame {frame}: Difference areas annotation"
    label3 = f"Frame {frame}: Annotation Rick"
    label4 = f"Frame {frame}: My own annotation"
    imList = [(imName1,label1),(imName2,label2),(imName3,label3),(imName4,label4)]

    #The first image: the base oct frame
    makeImage(oct_frame, None, imName1)

    #The second image: the differences
    diff_im = np.abs(np.copy(my_frame)-np.copy(rick_frame))
    diff_im[diff_im>0]=1
    makeImage(oct_frame,diff_im,imName2)

    #The third image: Rick's annotation
    getPred(rick_frame,None,imName3)
    #The fourth image: My annotation
    getPred(my_frame,None,imName4)

    ####################
    return imList

def makeImage(frame,overlay,imName):
    if overlay is not None:
        frame[overlay==1] = [255,0,0]
    data = im.fromarray(frame)
      
    # saving the final output 
    # as a PNG file
    data.save(imName)

def add_pred_overlay(oct_frame,pred_frame,label_interest,color):
    frameDouble = np.copy(oct_frame)
    #toOverlay = np.zeros((pred_frame.shape[0],pred_frame.shape[1],3))
    frameDouble[pred_frame==label_interest]=color
    
    return frameDouble

def getPred(pred_frame, overlay, imName):
    #Specify color map
    color_map = {
    0: (0, 0, 0),        #background
    1: (255, 0, 0),      #lumen
    2: (63, 63, 63),      #guide
    3: (0, 0, 255),      #intima
    4: (255, 255, 0),    #lipid
    5: (255, 255, 255),  #calcium
    6: (255, 0, 255),    #media
    7: (146, 0, 0),      #catheter
    8: (255, 123, 0),    #sidebranch
    9: (230, 141, 230),  #red thrombus
    10: (0, 255, 255),   #white thrombus
    11: (65, 135, 100),  #Dissection
    12: (208, 190, 161), #rupture
    13: (0,255,0),       #Healed plaque
    14: (162,162,162),   #Neovascularization
    }

    #Convert the labels array into a color-coded image
    h, w = pred_frame.shape
    color_img = np.zeros((h, w, 3), dtype=np.uint8)
    for label, color in color_map.items():
        color_img[pred_frame == label] = color

    makeImage(color_img,overlay,imName)