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
                
            self.load_augmentations()
                
            
    def load_augmentations(self):
        """
        Load the augmentations into the data set
        
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
        
        
    def vocab(self, mode):
        """
        Create vacabulary file
        
        Input:
            - mode = "tr" for a transcription task, "de" for a decipherment task
        
        """ 
        
        # Alphabet from text files
        if mode == "tr":
            self.alphabet = utils.uniqueValues(self.txtSavepath, self.txtFiles) 
        if mode == "de":
            self.alphabet = utils.uniqueCharacters(self.txtSavepath, self.txtFiles) 
        
        # Create json structure
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
        
        
    def load_dataset(self, pTrain, pTest, mode):
        """
        Load data set
        
        Inputs:
            - pTrain = Percentage for train set (int)
            - pTest = Percentage for test set (int)
            - mode = "tr" for a transcription task, "de" for a decipherment task
            
        """
        # Load data
        self.load_data()
        
        # Vocab file
        self.vocab(mode)
        
        # Split dataset
        self.split_train_test_valid(pTrain, pTest)
    
    
    def load_json_only(self, pTrain, pTest, mode):
        """
        Load data set, without loading the images into the folder
        
        Inputs:
            - pTrain = Percentage for train set (int)
            - pTest = Percentage for test set (int)
            - mode = "tr" for a transcription task, "de" for a decipherment task
            
        """
        # Create folder
        if not os.path.exists(self.root):
            os.makedirs(self.root)
            
        # Load Augmentations
        if self.sizeAug != 0:
            self.load_augmentations()
        
        # Vocab file
        self.vocab(mode)
        
        # Split dataset
        self.split_train_test_valid(pTrain, pTest)
        
        
        
        
class LoadDatasetCustom:
    
    def __init__(self, root, train_img_savepath, train_txt_savepath, nTrain,
                             test_img_savepath, test_txt_savepath, nTest,
                             train_aug_savepath=0, test_aug_savepath=0):
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
        
        # Train files
        self.train_img_savepath = train_img_savepath
        self.train_img_files = os.listdir(train_img_savepath)[0:nTrain]
        
        self.train_txt_savepath = train_txt_savepath
        self.train_txt_files = os.listdir(train_txt_savepath)[0:nTrain]    
        
        self.nTrain = nTrain
        
        # Test files
        self.test_img_savepath = test_img_savepath
        self.test_img_files = os.listdir(test_img_savepath)[0:nTest]
        
        self.test_txt_savepath = test_txt_savepath
        self.test_txt_files = os.listdir(test_txt_savepath)[0:nTest]

        self.nTest = nTest

        # Train Augmentation files
        if train_aug_savepath == 0:
            self.nTrainAug = 0
        else:
            self.train_aug_savepath = train_aug_savepath
            self.train_aug_files = os.listdir(train_aug_savepath)
            
            self.nTrainAug = len(self.train_aug_files)
            self.trainMultiplicator = int(self.nTrainAug / nTrain)
            
        # Test Augmentation files
        if test_aug_savepath == 0:
            self.nTestAug = 0
        else:
            self.test_aug_savepath = test_aug_savepath
            self.test_aug_files = os.listdir(test_aug_savepath)
            
            self.nTestAug = len(self.test_aug_files)
            self.testMultiplicator = int(self.nTestAug / nTest)
        

    def load_data(self):
        """
        Load images into the data set folder
        
        """ 
        # Create folder
        if not os.path.exists(self.root + "/lines/"):
            os.makedirs(self.root + "/lines/")
        
        
        # Load Train Images into file
        print("Moving train images into folder data...")
        
        for imgChar in self.train_img_files:
            im = Image.open(self.train_img_savepath + imgChar)
            im.save(self.root + "/lines/train_" + imgChar,"PNG")
           
            
        # Load Train Augmentations
        if self.nTrainAug != 0:
            print("Moving augmented train images into folder data...")
            
            for imgChar in self.train_aug_files:
                im = Image.open(self.train_aug_savepath + imgChar)
                im.save(self.root + "/lines/train_" + imgChar,"PNG")
                
            self.load_augmentations("train")
            
            
        # Load Test Images into file
        print("Moving test images into folder data...")
        
        for imgChar in self.test_img_files:
            im = Image.open(self.test_img_savepath + imgChar)
            im.save(self.root + "/lines/test_" + imgChar,"PNG")
           
            
        # Load Test Augmentations
        if self.nTestAug != 0:
            print("Moving augmented test images into folder data...")
            
            for imgChar in self.test_aug_files:
                im = Image.open(self.test_aug_savepath + imgChar)
                im.save(self.root + "/lines/test_" + imgChar,"PNG")
                
            self.load_augmentations("test")
            
            
    def load_augmentations(self, mode):
        """
        Load the augmentations into the data set
        
        """ 
            
        if mode == "train":
            # Augment image files
            augImgFiles = self.train_img_files + self.train_aug_files
            self.train_img_files = augImgFiles
            self.train_img_files.sort()
            
            # Augment text files
            augTextFiles = []
            
            for txt in self.train_txt_files:
                for i in range(self.trainMultiplicator + 1):
                    augTextFiles.append(txt)
                    
            self.train_txt_files = augTextFiles
            
            
        if mode == "test":
            # Augment image files
            augImgFiles = self.test_img_files + self.test_aug_files
            self.test_img_files = augImgFiles
            self.test_img_files.sort()
            
            # Augment text files
            augTextFiles = []
            
            for txt in self.test_txt_files:
                for i in range(self.testMultiplicator + 1):
                    augTextFiles.append(txt)
                    
            self.test_txt_files = augTextFiles
        
        
    def vocab(self, mode):
        """
        Create vacabulary file
        
        Input:
            - mode = "tr" for a transcription task, "de" for a decipherment task
        
        """ 
        
        # Alphabet from text files
        if mode == "tr":
            self.alphabet = utils.uniqueValues(self.train_txt_savepath, self.train_txt_files) 
        if mode == "de":
            self.alphabet = utils.uniqueCharacters(self.train_txt_savepath, self.train_txt_files) 
        
        # Create json structure
        vocabulary = {}
        vocabulary["labels"] = self.alphabet.tolist()
        vocab = json.dumps(vocabulary)
        
        # Save vocab file
        print("Saving vocab file...")
        f = open(self.root + "vocab.json", "w")
        f.write(vocab)
        f.close()
        
        
    def split_train_test_valid(self, pTrain, pTest, mode):
        """
        Split samples into train-test-validation and save in a json file
        
        Inputs:
            - pTrain = Percentage for train set (int)
            - pTest = Percentage for test set (int)
            - mode = "tr" for a transcription task, "de" for a decipherment task
            
        """
        # Dictionaries
        train = {}
        test = {}
        valid = {}
        
        
        # Shuffle data
        zipped = list(zip(self.train_txt_files, self.train_img_files))
        random.shuffle(zipped)
        trainTxt, trainImg = zip(*zipped)
        
        # Take desired percentage of train
        trainTxt = trainTxt[0:math.floor(self.nTrain*pTrain)]
        trainImg = trainImg[0:math.floor(self.nTrain*pTrain)]
        
        # Fill dictionary
        for txt, im in zip(trainTxt, trainImg):
            atr = {}
            t = open(self.train_txt_savepath + txt, "r")
            atr["ts"] = t.read()
            t.close()
            
            train["train_" + im] = atr
        
        
        # Shuffle data
        zipped = list(zip(self.test_txt_files, self.test_img_files))
        random.shuffle(zipped)
        testvalidTxt, testvalidImg = zip(*zipped)
        
        # Take desired percentage of train and validation
        testTxt = testvalidTxt[0:math.floor(self.nTest*pTest/2)]
        testImg = testvalidImg[0:math.floor(self.nTest*pTest/2)]        
        validTxt = testvalidTxt[math.floor(self.nTest*pTest/2)+1:]
        validImg = testvalidImg[math.floor(self.nTest*pTest/2)+1:]        
        
        # Fill dictionaries
        for txt, im in zip(testTxt, testImg):
            atr = {}
            t = open(self.test_txt_savepath + txt, "r")
            atr["ts"] = t.read()
            t.close()
            
            test["test_" + im] = atr

        for txt, im in zip(validTxt, validImg):
            atr = {}
            t = open(self.test_txt_savepath + txt, "r")
            atr["ts"] = t.read()
            t.close()
            
            valid["test_" + im] = atr
        
        
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
        
        
    def load_dataset(self, pTrain, pTest, mode):
        """
        Load data set
        
        Inputs:
            - pTrain = Percentage for train set (int)
            - pTest = Percentage for test set (int)
            - mode = "tr" for a transcription task, "de" for a decipherment task
            
        """
        # Load data
        self.load_data()
        
        # Vocab file
        self.vocab(mode)
        
        # Split dataset
        self.split_train_test_valid(pTrain, pTest, mode)
    
    
    def load_json_only(self, pTrain, pTest, mode):
        """
        Load data set, without loading the images into the folder
        
        Inputs:
            - pTrain = Percentage for train set (int)
            - pTest = Percentage for test set (int)
            - mode = "tr" for a transcription task, "de" for a decipherment task
            
        """
        # Create folder
        if not os.path.exists(self.root):
            os.makedirs(self.root)
            
        # Load Augmentations
        if self.nTrainAug != 0:
            self.load_augmentations("train")
        if self.nTestAug != 0:
            self.load_augmentations("test")
        
        # Vocab file
        self.vocab(mode)
        
        # Split dataset
        self.split_train_test_valid(pTrain, pTest, mode)
        
        
        
        