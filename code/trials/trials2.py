# -*- coding: utf-8 -*-

import json
import numpy as np
import math
import os


def uniqueValues(path, listFiles):
    """
    Get unique values from text files
    
    """
    listChars = []
    
    for file in listFiles:
        
        # Read line
        f = open(path + file, "r", encoding="UTF-8")
        line = f.read()
        f.close()
        
        # Add to list
        listChars.extend(line.split(" "))
        
    # Return unique value
    return np.unique(listChars)


if __name__ == '__main__':
    """
    alphabet = uniqueValues("../../databases/copiale_real-vs-sint/sint/transcriptions/", 
                            os.listdir("../../databases/copiale_real-vs-sint/sint/transcriptions/")[0:500])
    
    d = {}
    d["labels"] = alphabet.tolist()
    
    vocab = json.dumps(d)
    """
    
    size = 500
    
    nTrain = math.floor(size*0.8)
    nValid = math.floor(size*0.1)
    nTest = math.floor(size*0.1)
    
    txtFiles = list(range(size))
    content = list(range(size))
    
    #train = txtFiles[0:nTrain]
    #valid = txtFiles[nTrain:nTrain+nValid]
    #test = txtFiles[nTrain+nValid:]
    
    
    text = {}
    for ln, txt in zip(content, txtFiles):
        line = {}
        line["segm"] = 0
        line["ts"] = ln
        
        text[txt] = line
    
    