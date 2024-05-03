## -*- coding: utf-8 -*-

import os
import utils
import json
import math
from PIL import Image


class LoadDataset:
    
    def __init__(self, root, size, imgSavepath, txtSavepath):
        """
        Initialization of class values
        
        Inputs: 
            - root = 
            - alphabet = 
            - imFiles =
            - txtFiles
        
        """ 
        self.root = root
        self.size = size
        
        # Image files
        self.imgSavepath = imgSavepath
        self.imgFiles = os.listdir(imgSavepath)[0:size]
        
        # Text files 
        self.txtSavepath = txtSavepath
        self.txtFiles = os.listdir(txtSavepath)[0:size]
        
        # Alphabet from text files
        self.alphabet = utils.uniqueValues(txtSavepath, self.txtFiles)
        
        
    def loadDataset(self, pTrain, pTest):
        """
        ---
        
        """ 
        # Create folder
        if not os.path.exists(self.root + "/lines/"):
            os.makedirs(self.root + "/lines/")
        
        # Load images into file
        print("Moving images into folder data...")
        
        for imgChar in self.imgFiles:
            im = Image.open(self.imgSavepath + imgChar)
            im.save(self.root + "/lines/" + imgChar,"PNG")
        
        # Create vocab file
        vocabulary = {}
        vocabulary["labels"] = self.alphabet.tolist()
        vocab = json.dumps(vocabulary)
        
        # Save vocab file
        print("Saving vocab file...")
        f = open(self.root + "vocab.json","w")
        f.write(vocab)
        f.close()
        
        # Split train - validation - test
        nTrain = math.floor(self.size*pTrain)
        nTest = math.floor(self.size*pTest)
        
        trainTxt = self.txtFiles[0:nTrain]
        trainImg = self.imgFiles[0:nTrain]        
        train = {}
        
        testTxt = self.txtFiles[nTrain:nTrain+nTest]
        testImg = self.imgFiles[nTrain:nTrain+nTest]        
        test = {}
        
        validTxt = self.txtFiles[nTrain+nTest:]
        validImg = self.imgFiles[nTrain+nTest:]        
        valid = {}
        
        # Generation Train dictionary
        for txt, im in zip(trainTxt, trainImg):
            atr = {}
            atr["segm"] = None
            
            t = open(self.txtSavepath + txt, "r", encoding="UTF-8")
            atr["ts"] = t.read()
            t.close()
            
            train[im] = atr
        
        
        # Generation Test dictionary
        for txt, im in zip(testTxt, testImg):
            atr = {}
            atr["segm"] = None
            
            t = open(self.txtSavepath + txt, "r", encoding="UTF-8")
            atr["ts"] = t.read()
            t.close()
            
            test[im] = atr
            
            
        # Generation Validation dictionary
        for txt, im in zip(validTxt, validImg):
            atr = {}
            atr["segm"] = None
            
            t = open(self.txtSavepath + txt, "r", encoding="UTF-8")
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
        
        