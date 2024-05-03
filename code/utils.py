# -*- coding: utf-8 -*-

import numpy as np

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