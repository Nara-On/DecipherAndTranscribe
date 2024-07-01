# -*- coding: utf-8 -*-

from PIL import Image
import cv2
import numpy as np
import random
import os


class Augmentation:
    
    def __init__(self, multiplicator):
        """
        Initialization of class values
        
        """ 
        self.multiplicator = multiplicator
        
        self.param_gamma_low = .3
        self.param_gamma_high = 2

        self.param_mean_gaussian_noise = 0
        self.param_sigma_gaussian_noise = 100**0.5
        
        # Params controlling how much foreground and background pixels flip state
        self.param_kanungo_alpha = 2
        self.param_kanungo_beta = 2
        self.param_kanungo_alpha0 = 1
        self.param_kanungo_beta0 = 1
        self.param_kanungo_mu = 0
        self.param_kanungo_k = 2
        
        # Here a little bit more shear to the left than to the right
        self.param_min_shear = -.5
        self.param_max_shear = .25
        
        # Plus minus angles for rotation
        self.param_rotation = 3
        
        # One plus minus parameter as scaling factor
        self.param_scale = .2 
        
        # Translation for cropping errors in pixels
        self.param_movement_BB = 6
        
        
    def variation(self, img):
        """
        Create image variations
        
        Inputs: 
            - img = Original image (int array)
            
        Outputs:
            - final_img = Variation of original image (int array)
        
        """
        TH,TW=img.shape

        # Add gaussian noise
        gauss = np.random.normal(self.param_mean_gaussian_noise, self.param_sigma_gaussian_noise,(TH,TW))
        gauss = gauss.reshape(TH,TW)
        gaussiannoise = np.uint8(np.clip(np.float32(img) + gauss,0,255))

        # Randomly erode, dilate or nothing
        kernel=np.ones((3,3), np.uint8)
        a=random.choice([2,3])
        
        if a==1:
            gaussiannoise = cv2.dilate(gaussiannoise, kernel, iterations=1)
        elif a==2:
            gaussiannoise = cv2.erode(gaussiannoise, kernel, iterations=1)

        # Add random gamma correction
        gamma = np.random.uniform(self.param_gamma_low, self.param_gamma_high)
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")
        gammacorrected = cv2.LUT(np.uint8(gaussiannoise), table)

        # Binarize image with Otsu
        otsu_th,binarized = cv2.threshold(gammacorrected,0,1,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        # Kanungo noise
        dist = cv2.distanceTransform(1-binarized, cv2.DIST_L1, 3)  # try cv2.DIST_L1 for newer versions of OpenCV
        dist2 = cv2.distanceTransform(binarized, cv2.DIST_L1, 3) # try cv2.DIST_L1 for newer versions of OpenCV

        dist = dist.astype('float64') # Tro add
        dist2 = dist2.astype('float64') # Tro add

        P = (self.param_kanungo_alpha0 * np.exp(-self.param_kanungo_alpha * dist**2)) + self.param_kanungo_mu
        P2 = (self.param_kanungo_beta0 * np.exp(-self.param_kanungo_beta * dist2**2)) + self.param_kanungo_mu
        distorted = binarized.copy()
        distorted[((P>np.random.rand(P.shape[0],P.shape[1])) & (binarized==0))] = 1
        distorted[((P2>np.random.rand(P.shape[0],P.shape[1])) & (binarized==1))] = 0
        closing = cv2.morphologyEx(distorted, cv2.MORPH_CLOSE, np.ones((self.param_kanungo_k, self.param_kanungo_k), dtype=np.uint8))

        # Apply binary image as mask and put it on a larger canvas
        pseudo_binarized = closing * (255-gammacorrected)
        canvas = np.zeros((3*TH,3*TW),dtype=np.uint8)
        canvas[TH:2*TH,TW:2*TW] = pseudo_binarized
        points = []
        
        count = 0 # Tro add
        while(len(points)<1):
            count += 1 # Tro add
            if count > 50: # Tro add
                break # Tro add

            # Random shear
            shear_angle=np.random.uniform(self.param_min_shear,self.param_max_shear)
            M=np.float32([[1,shear_angle,0],[0,1,0]])
            sheared = cv2.warpAffine(canvas,M,(3*TW,3*TH),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_CUBIC)

            # Random rotation
            M = cv2.getRotationMatrix2D((3*TW/2,3*TH/2), np.random.uniform(-self.param_rotation, self.param_rotation), 1)
            rotated = cv2.warpAffine(sheared, M, (3*TW,3*TH), flags=cv2.WARP_INVERSE_MAP|cv2.INTER_CUBIC)

            # Random scaling
            scaling_factor = np.random.uniform(1 - self.param_scale, 1 + self.param_scale)
            scaled = cv2.resize(rotated, None, fx = scaling_factor, fy = scaling_factor, interpolation=cv2.INTER_CUBIC)

            # Detect cropping parameters
            points = np.argwhere(scaled!=0)
            points = np.fliplr(points)

        if len(points) < 1: # Tro add
            return pseudo_binarized

        r = cv2.boundingRect(np.array([points]))

        # Random cropping
        deltax = random.randint(-self.param_movement_BB, self.param_movement_BB)
        deltay = random.randint(-self.param_movement_BB, self.param_movement_BB)
        x1 = min(scaled.shape[0]-1,max(0,r[1]+deltax))
        y1 = min(scaled.shape[1]-1,max(0,r[0]+deltay))
        x2 = min(scaled.shape[0],x1+r[3])
        y2 = min(scaled.shape[1],y1+r[2])
        final_image = np.invert(np.uint8(scaled[x1:x2,y1:y2]))
        
        return final_image
    
    
    def augmentator_txt(self, img_path, txt_path, img_savepath, txt_savepath):
        """
        Apply augmentation in a list of images and texts
        
        Inputs: 
            - img_path = Directory whith the original images (string)
            - txt_path = Directory whith the transcriptions (string)
            - img_savepath = Directory where the new images will be saved (string)
            - txt_savepath = Directory where the new gt will be saved (string)
        
        """
        
        # File names
        imList = os.listdir(img_path)
        txtList = os.listdir(txt_path) 
        
        # Generate directories if necessary
        if not os.path.exists(img_savepath):
            os.makedirs(img_savepath)

        if not os.path.exists(txt_savepath):
            os.makedirs(txt_savepath)
            
        for im, txt in zip(imList, txtList):
            print("Generating variations from image " + im)
            original = cv2.imread(img_path + im, 0)
            line = open(txt_path + txt, "r").read()
            
            for i in range(0, self.multiplicator):
                # Image Operations
                image = cv2.resize(self.variation(original), (original.shape[1], original.shape[0]), interpolation=cv2.INTER_AREA)
                image = Image.fromarray(image)
                
                image.save(img_savepath + im.split(".")[0] + '_' + str(i) + '.png',"PNG")
                
                # Text Operations
                f = open(txt_savepath + txt.split(".")[0] + '_' + str(i) + '.txt', "w")
                f.write(line)
                f.close()  
    
    
    def augmentator_img(self, img_path, img_savepath):
        """
        Apply augmentation in a list of images
        
        Inputs: 
            - img_path = Directory whith the original images (string)
            - img_savepath = Directory where the new images will be saved (string)
        
        """
        # File names
        imList = os.listdir(img_path)
        
        # Generate directories if necessary
        if not os.path.exists(img_savepath):
            os.makedirs(img_savepath)

            
        for im in imList:
            print("Generating variations from image " + im)
            original = cv2.imread(img_path + im, 0)
            
            for i in range(0, self.multiplicator):
                # Image Operations
                image = cv2.resize(self.variation(original), (original.shape[1], original.shape[0]), interpolation=cv2.INTER_AREA)
                image = Image.fromarray(image)
                
                image.save(img_savepath + im.split(".")[0] + '_' + str(i) + '.png',"PNG")
                
    
    
    