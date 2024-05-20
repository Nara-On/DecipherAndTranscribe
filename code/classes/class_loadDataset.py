## -*- coding: utf-8 -*-

import os
import utils
import json
import math
import random 
from PIL import Image


class LoadDataset:
    
    def __init__(self, root, sizeImg, imgSavepath, txtSavepath, augSavepath=0):
        """
        Initialization of class values
        
        Inputs: 
            - root = Root folder where the data set will be loaded (str)
            - sizeImg = Number of images in the future data set (int)
            - imgSavepath = Path where the images are stored (str)
            - txtSavepath = Path where the texts are stored (str)
            - augSavepath = Path where the augmentations of the images are stored, if needed (str, default=0)
        
        """ 
        self.root = root
        self.sizeImg = sizeImg
        
        # Image files
        self.imgSavepath = imgSavepath
        self.imgFiles = os.listdir(imgSavepath)[0:sizeImg]
        
        # Text files 
        self.txtSavepath = txtSavepath
        self.txtFiles = os.listdir(txtSavepath)[0:sizeImg]
        
        # Augmentation files
        if augSavepath == 0:
            self.sizeAug = 0
        else:
            self.augSavepath = augSavepath
            self.augFiles = os.listdir(augSavepath)
            self.sizeAug = len(self.augFiles)
            self.multiplicator = int(self.sizeAug / self.sizeImg)
            
        self.size = self.sizeImg + self.sizeAug
        

    def load_data(self):
        """
        Load images into the data set folder
        
        """ 
        # Create folder
        if not os.path.exists(self.root + "/lines/"):
            os.makedirs(self.root + "/lines/")
        
        # Load images into file
        print("Moving images into folder data...")
        
        for imgChar in self.imgFiles:
            im = Image.open(self.imgSavepath + imgChar)
            im.save(self.root + "/lines/" + imgChar,"PNG")
           
        # Load Augmentations
        if self.sizeAug != 0:
            print("Moving augmented images into folder data...")
            
            for imgChar in self.augFiles:
                im = Image.open(self.augSavepath + imgChar)
                im.save(self.root + "/lines/" + imgChar,"PNG")
                
            self.load_augmentation_files()
                
            
    def load_augmentation_files(self):
        """
        Load the augmentations of the images into the data set
        
        """ 
            
        # Augment image files
        augImgFiles = self.imgFiles + self.augFiles
        self.imgFiles = augImgFiles
        self.imgFiles.sort()
        
        # Augment text files
        augTextFiles = []
        
        for txt in self.txtFiles:
            for i in range(self.multiplicator + 1):
                augTextFiles.append(txt)
                
        self.txtFiles = augTextFiles
        
        
    def vocab_tr(self):
        """
        Create vacabulary file for transcription task
        
        """ 
        
        # Transcription alphabet from text files
        self.alphabet = utils.uniqueValues(self.txtSavepath, self.txtFiles) 
        
        # Create json structure
        vocabulary = {}
        vocabulary["labels"] = self.alphabet.tolist()
        vocab = json.dumps(vocabulary)
        
        # Save vocab file
        print("Saving vocab file...")
        f = open(self.root + "vocab.json", "w")
        f.write(vocab)
        f.close()
        
    
    def vocab_de(self):
        """
        Create vacabulary file for decipherment task
        
        """ 
        # Decipherment alphabet from text files
        self.alphabet = utils.uniqueCharacters(self.txtSavepath, self.txtFiles) 
        
        vocabulary = {}
        vocabulary["labels"] = self.alphabet.tolist()
        vocab = json.dumps(vocabulary)
        
        # Save vocab file
        print("Saving vocab file...")
        f = open(self.root + "vocab.json", "w")
        f.write(vocab)
        f.close()
        
        
    def split_train_test_valid(self, pTrain, pTest):
        """
        Split samples into train-test-validation and save in a json file
        
        Inputs:
            - pTrain = Percentage for train set (int)
            - pTest = Percentage for test set (int)
            
        """

        zipped = list(zip(self.txtFiles, self.imgFiles))
        random.shuffle(zipped)
        txts, imgs = zip(*zipped)
        
        
        # Split train - validation - test
        nTrain = math.floor(self.size*pTrain)
        nTest = math.floor(self.size*pTest)
        
        trainTxt = txts[0:nTrain]
        trainImg = imgs[0:nTrain]        
        train = {}
        
        testTxt = txts[nTrain:nTrain+nTest]
        testImg = imgs[nTrain:nTrain+nTest]        
        test = {}
        
        validTxt = txts[nTrain+nTest:]
        validImg = imgs[nTrain+nTest:]        
        valid = {}
        
        # Generation Train dictionary
        for txt, im in zip(trainTxt, trainImg):
            atr = {}
            t = open(self.txtSavepath + txt, "r")
            atr["ts"] = t.read()
            t.close()
            
            train[im] = atr
        
        
        # Generation Test dictionary
        for txt, im in zip(testTxt, testImg):
            atr = {}
            t = open(self.txtSavepath + txt, "r")
            atr["ts"] = t.read()
            t.close()
            
            test[im] = atr
            
            
        # Generation Validation dictionary
        for txt, im in zip(validTxt, validImg):
            atr = {}
            t = open(self.txtSavepath + txt, "r")
            atr["ts"] = t.read()
            t.close()
            
            valid[im] = atr
        
        
        # Save files train - validation - test
        trainJson = json.dumps(train)
        testJson = json.dumps(test)
        validJson = json.dumps(valid)
        
        print("Saving train groundtruth files...")
        f = open(self.root + "gt_training.json","w")
        f.write(trainJson)
        f.close()
        
        print("Saving test groundtruth files...")
        f = open(self.root + "gt_testing.json","w")
        f.write(testJson)
        f.close()
        
        print("Saving validation groundtruth files...")
        f = open(self.root + "gt_validation.json","w")
        f.write(validJson)
        f.close()
        
        
    def load_dataset_tr(self, pTrain, pTest):
        """
        Load data set for a transcription task
        
        Inputs:
            - pTrain = Percentage for train set (int)
            - pTest = Percentage for test set (int)
            
        """
        # Load data
        self.load_data()
        
        # Vocab file
        self.vocab_tr()
        
        # Split dataset
        self.split_train_test_valid(pTrain, pTest)
        
        
    def load_dataset_de(self, pTrain, pTest):
        """
        Load data set for a decipherment task
        
        Inputs:
            - pTrain = Percentage for train set (int)
            - pTest = Percentage for test set (int)
            
        """
        # Load data
        self.load_data()
        
        # Vocab file
        self.vocab_de()
        
        # Split dataset
        self.split_train_test_valid(pTrain, pTest)
    
    
    def redo_files_tr(self, pTrain, pTest):
        """
        Load data set for a transcription task, without loading the images
        
        Inputs:
            - pTrain = Percentage for train set (int)
            - pTest = Percentage for test set (int)
            
        """
        # Load Augmentations
        if self.sizeAug != 0:
            self.load_augmentation_files()
        
        # Vocab file
        self.vocab_tr()
        
        # Split dataset
        self.split_train_test_valid(pTrain, pTest)
    
    
    def redo_files_de(self, pTrain, pTest):
        """
        Load data set for a decipherment task, without loading the images
        
        Inputs:
            - pTrain = Percentage for train set (int)
            - pTest = Percentage for test set (int)
            
        """
        # Load Augmentations
        if self.sizeAug != 0:
            self.load_augmentation_files()
            
        # Vocab file
        self.vocab_de()
        
        # Split dataset
        self.split_train_test_valid(pTrain, pTest)
        
        
        
        