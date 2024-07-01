# -*- coding: utf-8 -*-

import numpy as np


# Exceptions: Values that describe one character
exceptions = ["*o*", "*star*", "*nee*", "*tri*", "*bigx*", "*gate*", "*lip*", "*bigl*", "*tribig*",
              "*sci*", "*toe*", "*krussedull*",
              
              "Alkali", "BallotScriptX", "BigC", "BigF", "BigH", "BigInsularD", 
              "BigK", "BigN", "BigV", "CapitalGamma", "CapitalLambda", "CircledEquals", "Dagger", "Earth", 
              "Female", "Fire", "Infinity", "InsularD", "Integral", "LatinLongLigatureFi", "LatinSmallLigatureFi",
              "NorthEastArrow", "NotEqualTo", "PhoenicianLetterPe", "RockSalt", "Saturn", "ScriptSmallG", 
              "ScriptSmallZ", "SleepingSymbol", "SmallDelta", "SmallIota", "SmallNHook", "SmallPi", 
              "SquareP", "SquaredPlus", "SquaredRisingDiagonalSlash", "TF", "TopHalfIntegral", "TriangleDot"
              "UpwardsArrow", "VerticalLine", 
              
              "a^^", "c^.", "e?", "e^^", "h^.", "i^^", "m^.", "m__", "n^.", "n__", "o^.", "o^^", "p^.", "r^.",
              "r__", "s^.", "u^^", "u__", "x^.", "y^..", "%%%%"]
    


def uniqueValues(path, listFiles):
    """
    Get unique values from text files
    
    """
    listChars = []
    
    for file in listFiles:
        # Read line
        f = open(path + file, "r")
        line = f.read()
        f.close()
        
        # Add to list
        listChars.extend(line.split(" "))
       
    # Add space to list
    listChars.append(" ")
    
    # Return unique value
    return np.unique(listChars)


def uniqueCharacters(path, listFiles):
    """
    Get unique characters from text files, without including the exceptions
    
    """
    listChars = []
    
    for file in listFiles:
        # Read line
        f = open(path + file, "r")
        line = f.read()
        f.close()
        
        listChars.extend(list(line))
        
        """        
        # Add to list
        words = line.split(" ")
        

        for w in words:
            if w in exceptions:
                listChars.append(w)
            else:
                listChars.extend(w)
        """
        
    listChars.append(" ")
    
    # Return unique value
    return np.unique(listChars)



