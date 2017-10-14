# P4_util.py
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import os.path as osp
import glob

def getCalibration(img_list):
    nx,ny = 9,6
    # --- convert the image to grayscale
    
    objpts_list = list()
    imgpts_list = list()
    
    objpts = np.zeros((nx*ny,3),np.float32)
    objpts[:,:2] = np.mgrid[0:nx,0:ny].T.reshape(-1,2)
    
    img_shape = (img_list[0].shape[1],img_list[0].shape[0])
    for ii,img in enumerate(img_list):
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # --- Find the chessboard corners
        # ret is simply a boolean return value that is true if the corners are found and false if otherwise
        foundCorners, imgpts = cv2.findChessboardCorners(gray, (nx,ny), None)
    
    
        if foundCorners:
            # --- Prepare object points, (0,0,0), (1,0,0), (2,0,0), ... , (7,5,0)
            # initialize nx X ny of 3-tuples (x,y,z) with all zeros 
            
            objpts_list.append(objpts)
            imgpts_list.append(imgpts)
            #---- draw
            img_cp = np.copy(img)
            cv2.drawChessboardCorners(img_cp, (nx,ny), imgpts, foundCorners)
            plt.figure(figsize=[15,15])
            plt.subplot(1,2,1)
            plt.imshow(img)
            plt.title("Original ({})".format(ii))
            
            plt.subplot(1,2,2)
            plt.imshow(img_cp)
            plt.title("With Corners")
            
    
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpts_list, imgpts_list, img_shape, None, None)
    return mtx,dist


