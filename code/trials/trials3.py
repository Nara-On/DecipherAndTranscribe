# -*- coding: utf-8 -*-

import os
import numpy as np
import json


def uniqueCharacters(path, listFiles):
    """
    Get unique values from text files
    
    """
    
    # Exceptions: Values that describe one character
    exceptions = ["*o*", "*star*", "*nee*", "*tri*", "*bigx*", "*gate*", "*lip*", "*lip*:", "*bigl*", "*tribig*",
                  "*tri..*", "*sci*", "*toe*", "*krussedull*",
                  
                  "Alkali", "BallotScriptX", "BigC", "BigF", "BigH", "BigInsularD", 
                  "BigK", "BigN", "BigV", "CapitalGamma", "CapitalLambda", "CircledEquals", "Dagger", "Earth", 
                  "Female", "Fire", "Infinity", "InsularD", "Integral", "LatinLongLigatureFi", "LatinSmallLigatureFi",
                  "NorthEastArrow", "NotEqualTo", "PhoenicianLetterPe", "RockSalt", "Saturn", "ScriptSmallG", 
                  "ScriptSmallZ", "SleepingSymbol", "SmallDelta", "SmallIota", "SmallNHook", "SmallPi", 
                  "SquareP", "SquaredPlus", "SquaredRisingDiagonalSlash", "TF", "TopHalfIntegral", "TriangleDot"
                  "UpwardsArrow", "VerticalLine", 
                  
                  "a^^", "c^.", "e?", "e^^", "h^.", "i^^", "m^.", "m__", "n^.", "n__", "o^.", "o^^", "p^.", "r^.",
                  "r__", "s^.", "u^^", "u__", "x^.", "y^..", "%%%%"]
    
    
    listChars = []
    
    for file in listFiles:
        # Read line
        f = open(path + file, "r")
        line = f.read()
        f.close()
        
        # Add to list
        words = line.split(" ")
        
        for w in words:
            if w in exceptions:
                listChars.append(w)
            else:
                listChars.extend(w)
        
    listChars.append(" ")
    
    # Return unique value
    return np.unique(listChars)



if __name__ == '__main__':
    
    file = "../../databases/copiale_real-vs-sint/real/deciphered/d2_0574.txt"
    
    f = open(file, "r")
    #line = f.read()

    atr = {}
    atr["ex"] = f.read()
    f.close()    
    
    trainJson = json.dumps(atr) 
    
    ######################
    
    
    path = "../../databases/copiale_real-vs-sint/real/deciphered/"
    files = os.listdir(path)[0:1502]
    
    unChar = uniqueCharacters(path, files)
    
    listChars = []
    
    exceptions = ["Alkali", "sci", "toe"]
    words = ["secret", "is", "not", "Alkali", "but", "from", "sci", "not", "gate"]
    sentence = "secret is not Alkali but from sci not gate"
    
    for w in words:
        if w in exceptions:
            listChars.append(w)
        else:
            listChars.extend(w)
        listChars.append(" ")
    
    
    
    
    