# -*- coding: utf-8 -*-

import os
import json
import numpy as np
import math

from numpy.typing import ArrayLike
from typing import List, Tuple, Union
from torchmetrics.text import CharErrorRate


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


def maxString(path, listFiles):
    """
    ---
    
    """
    listChars = []
    
    for file in listFiles:
        
        # Read line
        f = open(path + file, "r")
        line = f.read()
        f.close()
        
        # Add to list
        listChars.append(line)
        
    # Return unique value
    return max(listChars, key=len) 


def maxWords(path, listFiles):
    """
    ---
    
    """
    listChars = []
    
    for file in listFiles:
        
        # Read line
        f = open(path + file, "r")
        line = f.read()
        f.close()
        
        # Add to list
        listChars.append(line.split(" "))
        
    # Return unique value
    return max(listChars, key=len) 


def decodePred(encoded, error):
    index2vocab = {0: '<BLANK>', 1: '<GO>', 2: '<STOP>', 3: '<PAD>', 4: '"', 5: '%%', 6: '%%%', 7: '%%%%%', 8: '(', 9: '(:', 10: ')', 11: '*krussedull*', 12: '+', 13: '.', 14: '..', 15: '...', 16: '3', 17: ':', 18: ':)', 19: '=', 20: '@', 21: 'Alkali', 22: 'BallotScriptX', 23: 'BigB', 24: 'BigC', 25: 'BigD', 26: 'BigF', 27: 'BigFire', 28: 'BigG', 29: 'BigH', 30: 'BigInsularD', 31: 'BigJ', 32: 'BigK', 33: 'BigL', 34: 'BigM', 35: 'BigN', 36: 'BigP', 37: 'BigQ', 38: 'BigR', 39: 'BigS', 40: 'BigT', 41: 'BigV', 42: 'BigW', 43: 'BigZ', 44: 'CapitalGamma', 45: 'CapitalLambda', 46: 'CircledEquals', 47: 'Cloud', 48: 'Dagger', 49: 'Dissolve', 50: 'Dissolve_Square', 51: 'Earth', 52: 'Eye', 53: 'Female', 54: 'Fire', 55: 'Infinity', 56: 'InsularD', 57: 'Integral', 58: 'LatinLongLigatureFi', 59: 'LatinSmallLigatureFi', 60: 'NorthEastArrow', 61: 'NotEqualTo', 62: 'Pentagram', 63: 'PhoenicianLetterPe', 64: 'PlainBigL', 65: 'RockSalt', 66: 'Saturn', 67: 'ScriptSmallG', 68: 'ScriptSmallZ', 69: 'SleepingSymbol', 70: 'SmallDelta', 71: 'SmallIota', 72: 'SmallNHook', 73: 'SmallPi', 74: 'SquareP', 75: 'SquaredPlus', 76: 'SquaredRisingDiagonalSlash', 77: 'TopHalfIntegral', 78: 'TriangleDot', 79: 'UpwardsArrow', 80: 'VerticalLine', 81: 'a', 82: 'a^^', 83: 'b', 84: 'c', 85: 'c^.', 86: 'd', 87: 'e', 88: 'e?', 89: 'e^^', 90: 'f', 91: 'g', 92: 'gate', 93: 'h', 94: 'h^.', 95: 'i', 96: 'i^^', 97: 'j', 98: 'k', 99: 'l', 100: 'm', 101: 'm^.', 102: 'm__', 103: 'n', 104: 'n^.', 105: 'n__', 106: 'o', 107: 'o^.', 108: 'o^^', 109: 'p', 110: 'p^.', 111: 'q', 112: 'qua', 113: 'r', 114: 'r^.', 115: 'r__', 116: 's', 117: 's^.', 118: 'sci', 119: 't', 120: 'u', 121: 'u^^', 122: 'u__', 123: 'v', 124: 'w', 125: 'x', 126: 'x^.', 127: 'y', 128: 'y^..', 129: 'z', 130: '{', 131: '}'}
    
    decoded = []
    for x in encoded:
        if x < len(index2vocab):
            decoded.append(index2vocab[x])
        else:
            decoded.append(error)    
    return decoded


def decode(encoded):
    index2vocab = {0: '<BLANK>', 1: '<GO>', 2: '<STOP>', 3: '<PAD>', 4: '"', 5: '%%', 6: '%%%', 7: '%%%%%', 8: '(', 9: '(:', 10: ')', 11: '*krussedull*', 12: '+', 13: '.', 14: '..', 15: '...', 16: '3', 17: ':', 18: ':)', 19: '=', 20: '@', 21: 'Alkali', 22: 'BallotScriptX', 23: 'BigB', 24: 'BigC', 25: 'BigD', 26: 'BigF', 27: 'BigFire', 28: 'BigG', 29: 'BigH', 30: 'BigInsularD', 31: 'BigJ', 32: 'BigK', 33: 'BigL', 34: 'BigM', 35: 'BigN', 36: 'BigP', 37: 'BigQ', 38: 'BigR', 39: 'BigS', 40: 'BigT', 41: 'BigV', 42: 'BigW', 43: 'BigZ', 44: 'CapitalGamma', 45: 'CapitalLambda', 46: 'CircledEquals', 47: 'Cloud', 48: 'Dagger', 49: 'Dissolve', 50: 'Dissolve_Square', 51: 'Earth', 52: 'Eye', 53: 'Female', 54: 'Fire', 55: 'Infinity', 56: 'InsularD', 57: 'Integral', 58: 'LatinLongLigatureFi', 59: 'LatinSmallLigatureFi', 60: 'NorthEastArrow', 61: 'NotEqualTo', 62: 'Pentagram', 63: 'PhoenicianLetterPe', 64: 'PlainBigL', 65: 'RockSalt', 66: 'Saturn', 67: 'ScriptSmallG', 68: 'ScriptSmallZ', 69: 'SleepingSymbol', 70: 'SmallDelta', 71: 'SmallIota', 72: 'SmallNHook', 73: 'SmallPi', 74: 'SquareP', 75: 'SquaredPlus', 76: 'SquaredRisingDiagonalSlash', 77: 'TopHalfIntegral', 78: 'TriangleDot', 79: 'UpwardsArrow', 80: 'VerticalLine', 81: 'a', 82: 'a^^', 83: 'b', 84: 'c', 85: 'c^.', 86: 'd', 87: 'e', 88: 'e?', 89: 'e^^', 90: 'f', 91: 'g', 92: 'gate', 93: 'h', 94: 'h^.', 95: 'i', 96: 'i^^', 97: 'j', 98: 'k', 99: 'l', 100: 'm', 101: 'm^.', 102: 'm__', 103: 'n', 104: 'n^.', 105: 'n__', 106: 'o', 107: 'o^.', 108: 'o^^', 109: 'p', 110: 'p^.', 111: 'q', 112: 'qua', 113: 'r', 114: 'r^.', 115: 'r__', 116: 's', 117: 's^.', 118: 'sci', 119: 't', 120: 'u', 121: 'u^^', 122: 'u__', 123: 'v', 124: 'w', 125: 'x', 126: 'x^.', 127: 'y', 128: 'y^..', 129: 'z', 130: '{', 131: '}'}
    
    a = []
    for x in encoded:
        a.append(index2vocab[x])
    return a


def levenshtein(
    source: Union[ArrayLike, str],
    target: Union[ArrayLike, str],
) -> Tuple[float, ArrayLike]:
    """Compute the Levenshtein distance between two strings.

    Parameters
    ----------
    source: Union[ArrayLike, str]
        An input sequence in a numpy array or a string.
    target: Union[ArrayLike, str]
        The sequence to compare to as a numpy array or a string.

    Returns
    -------
    float
        Levenshtein distance between both strings.
    ArrayLike
        Dynamic programming matrix for the string comparison process.
    """
    matrix = []

    if len(target) == 0:
        return len(source), np.array([])

    # We call tuple() to force strings to be used as sequences
    if not (isinstance(source, np.ndarray)):
        source = np.array(tuple(source))
    if not (isinstance(target, np.ndarray)):
        target = np.array(tuple(target))

    previous_row = np.arange(target.size + 1)

    matrix.append(previous_row)
    for s in source:
        current_row = previous_row + 1
        current_row[1:] = np.minimum(
            current_row[1:], np.add(previous_row[:-1], target != s)
        )
        current_row[1:] = np.minimum(current_row[1:], current_row[0:-1] + 1)

        previous_row = current_row
        matrix.append(previous_row)

    return previous_row[-1] / float(len(target)), np.array(matrix)



if __name__ == '__main__':
    """
    alphabet = uniqueValues("../../databases/copiale_real-vs-sint/sint/transcriptions/", 
                            os.listdir("../../databases/copiale_real-vs-sint/sint/transcriptions/")[0:500])
    
    d = {}
    d["labels"] = alphabet.tolist()
    
    vocab = json.dumps(d)

    
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
    
    """    
    ###########################################################################
    
    alphabetTr = uniqueValues("../../databases/copiale_real-vs-sint/sint/transcriptions/", 
                            os.listdir("../../databases/copiale_real-vs-sint/sint/transcriptions/")[0:1502])
    alphabetDe = uniqueCharacters("../../databases/copiale_real-vs-sint/real/deciphered/", 
                            os.listdir("../../databases/copiale_real-vs-sint/real/deciphered/")[0:1502])
    
    mostCharsTr = maxString("../../databases/copiale_real-vs-sint/sint/transcriptions/", 
                            os.listdir("../../databases/copiale_real-vs-sint/sint/transcriptions/")[0:1502])
    mostCharsDe = maxString("../../databases/copiale_real-vs-sint/real/deciphered/", 
                            os.listdir("../../databases/copiale_real-vs-sint/real/deciphered/")[0:1502])
    
    mostWordsTr = maxWords("../../databases/copiale_real-vs-sint/sint/transcriptions/", 
                            os.listdir("../../databases/copiale_real-vs-sint/sint/transcriptions/")[0:1502])
    mostWordsDec = maxWords("../../databases/copiale_real-vs-sint/real/deciphered/", 
                            os.listdir("../../databases/copiale_real-vs-sint/real/deciphered/")[0:1502])
    
    
    
    ###########################################################################

    preds_ex1 = [110, 110, 16, 16, 16, 16, 16, 93, 93, 93, 121, 115, 121, 163, 163, 73, 163, 163, 163, 185, 185, 115, 121, 163, 121, 101, 185, 121, 16, 115, 115, 73, 73, 114, 114, 101, 114, 16, 16, 16, 16, 16, 101, 44, 101, 16, 101, 121, 101, 121, 121, 115, 16, 115, 115, 115, 121, 114, 114, 101, 55, 121, 163, 93, 101, 163, 101, 121, 121, 121, 121, 121, 121, 121, 121, 16, 14, 86, 89, 121, 121, 163, 44, 44, 101, 73, 16, 16, 16, 163, 16, 121, 121, 121, 101, 163, 163, 163, 163, 163, 163, 163, 16, 16, 16, 115, 16, 16, 73, 71, 71, 71, 114, 114, 101, 101, 115, 115, 115, 121, 168, 114, 115, 121, 16, 16, 16, 16, 16, 89, 121, 16, 16, 16, 16, 44, 16, 16, 57, 16, 16, 101, 16, 16, 163, 16, 16, 16, 16, 16, 163, 163, 16, 16, 16, 16, 163, 163, 16, 16, 71, 71, 71, 16, 16, 16, 203, 121, 16, 16, 16, 121, 121, 121, 121, 121, 121, 121, 163, 44, 44, 134, 163, 115, 121, 136, 136, 73, 73, 73, 163, 73, 163, 73, 163, 121, 90, 16, 16]
    preds_ex2 = [63, 71, 146, 204, 94, 94, 152, 69, 124, 20, 197, 182, 130, 158, 192, 69, 69, 146, 146, 107, 130, 130, 152, 152, 58, 120, 58, 58, 58, 58, 122, 54, 54, 207, 152, 94, 122, 99, 56, 177, 177, 58, 58, 130, 146, 87, 87, 130, 130, 146, 130, 122, 122, 69, 69, 122, 160, 160, 58, 160, 160, 160, 160, 122, 122, 122, 160, 58, 58, 58, 58, 58, 177, 58, 58, 146, 58, 58, 182, 182, 177, 177, 182, 177, 157, 182, 54, 177, 40, 139, 130, 69, 58, 130, 160, 59, 56, 130, 30]
    preds_ex3 = [491, 267, 267, 466, 138, 321, 180, 180, 180, 378, 378, 378, 267, 381, 381, 0, 249, 409, 249, 249, 48, 48, 82, 479, 479, 117, 378, 249, 271, 271, 249, 271, 271, 321, 321, 321, 321, 271, 271, 410, 378, 378, 378, 180, 249, 378, 249, 381, 249, 271, 378, 321, 321, 321, 62, 249, 249, 249, 249, 484, 271, 321, 48, 267, 271, 267, 271, 48, 267, 180, 410, 271, 378, 271, 271, 62, 271, 62, 321, 321, 321, 48, 378, 378, 271, 249, 202, 202, 48, 378, 378, 62, 48, 271, 249, 378, 249, 48, 378, 320, 267, 180, 381, 381, 271, 62, 62, 229, 419, 321, 352, 352, 352, 48, 82, 285, 285, 378, 479, 466, 378, 378, 352, 352, 479, 258, 34, 249, 249, 378, 378, 249, 34, 34, 200, 229, 229, 48, 267, 271, 381, 82, 378, 378, 378, 133, 249, 192, 267, 267, 249, 378, 378, 321, 321, 321, 344, 369, 369, 321, 321, 420, 486, 352, 352, 321, 267, 321, 270, 270, 321, 82, 158, 158, 158, 158, 499, 378, 499, 249, 378, 423, 378, 484, 271, 62, 62, 249, 321, 321, 484, 378, 146, 270, 270, 271, 271, 271, 271]
    
    gt = [130, 123, 110, 64, 108, 13, 97, 46, 123, 96, 20, 92, 130, 68, 130, 123, 84, 46, 98, 73, 105, 116, 127, 20, 86, 82, 102, 108, 115, 72, 116, 18, 123, 94, 74, 90, 115, 85, 92, 95, 67, 13, 123]
    
    
    tokens = ['<BLANK>', '<GO>', '<STOP>', '<PAD>']
    vocab = ['<BLANK>', '<GO>', '<STOP>', '<PAD>', ' ', '"', '%%', '%%%', '%%%%%', '(', '(:', ')', '*krussedull*', '+', '.', '..', '...', '3', ':', ':)', '=', '@', 'Alkali', 'BallotScriptX', 'BigB', 'BigC', 'BigD', 'BigF', 'BigFire', 'BigG', 'BigH', 'BigInsularD', 'BigJ', 'BigK', 'BigL', 'BigM', 'BigN', 'BigP', 'BigQ', 'BigR', 'BigS', 'BigT', 'BigV', 'BigW', 'BigZ', 'CapitalGamma', 'CapitalLambda', 'CircledEquals', 'Cloud', 'Dagger', 'Dissolve', 'Dissolve_Square', 'Earth', 'Eye', 'Female', 'Fire', 'Infinity', 'InsularD', 'Integral', 'LatinLongLigatureFi', 'LatinSmallLigatureFi', 'NorthEastArrow', 'NotEqualTo', 'Pentagram', 'PhoenicianLetterPe', 'PlainBigL', 'RockSalt', 'Saturn', 'ScriptSmallG', 'ScriptSmallZ', 'SleepingSymbol', 'SmallDelta', 'SmallIota', 'SmallNHook', 'SmallPi', 'SquareP', 'SquaredPlus', 'SquaredRisingDiagonalSlash', 'TopHalfIntegral', 'TriangleDot', 'UpwardsArrow', 'VerticalLine', 'a', 'a^^', 'b', 'c', 'c^.', 'd', 'e', 'e?', 'e^^', 'f', 'g', 'gate', 'h', 'h^.', 'i', 'i^^', 'j', 'k', 'l', 'm', 'm^.', 'm__', 'n', 'n^.', 'n__', 'o', 'o^.', 'o^^', 'p', 'p^.', 'q', 'qua', 'r', 'r^.', 'r__', 's', 's^.', 'sci', 't', 'u', 'u^^', 'u__', 'v', 'w', 'x', 'x^.', 'y', 'y^..', 'z', '{', '}']
    vocab2index = {'<BLANK>': 0, '<GO>': 1, '<STOP>': 2, '<PAD>': 3, ' ': 4, '"': 5, '%%': 6, '%%%': 7, '%%%%%': 8, '(': 9, '(:': 10, ')': 11, '*krussedull*': 12, '+': 13, '.': 14, '..': 15, '...': 16, '3': 17, ':': 18, ':)': 19, '=': 20, '@': 21, 'Alkali': 22, 'BallotScriptX': 23, 'BigB': 24, 'BigC': 25, 'BigD': 26, 'BigF': 27, 'BigFire': 28, 'BigG': 29, 'BigH': 30, 'BigInsularD': 31, 'BigJ': 32, 'BigK': 33, 'BigL': 34, 'BigM': 35, 'BigN': 36, 'BigP': 37, 'BigQ': 38, 'BigR': 39, 'BigS': 40, 'BigT': 41, 'BigV': 42, 'BigW': 43, 'BigZ': 44, 'CapitalGamma': 45, 'CapitalLambda': 46, 'CircledEquals': 47, 'Cloud': 48, 'Dagger': 49, 'Dissolve': 50, 'Dissolve_Square': 51, 'Earth': 52, 'Eye': 53, 'Female': 54, 'Fire': 55, 'Infinity': 56, 'InsularD': 57, 'Integral': 58, 'LatinLongLigatureFi': 59, 'LatinSmallLigatureFi': 60, 'NorthEastArrow': 61, 'NotEqualTo': 62, 'Pentagram': 63, 'PhoenicianLetterPe': 64, 'PlainBigL': 65, 'RockSalt': 66, 'Saturn': 67, 'ScriptSmallG': 68, 'ScriptSmallZ': 69, 'SleepingSymbol': 70, 'SmallDelta': 71, 'SmallIota': 72, 'SmallNHook': 73, 'SmallPi': 74, 'SquareP': 75, 'SquaredPlus': 76, 'SquaredRisingDiagonalSlash': 77, 'TopHalfIntegral': 78, 'TriangleDot': 79, 'UpwardsArrow': 80, 'VerticalLine': 81, 'a': 82, 'a^^': 83, 'b': 84, 'c': 85, 'c^.': 86, 'd': 87, 'e': 88, 'e?': 89, 'e^^': 90, 'f': 91, 'g': 92, 'gate': 93, 'h': 94, 'h^.': 95, 'i': 96, 'i^^': 97, 'j': 98, 'k': 99, 'l': 100, 'm': 101, 'm^.': 102, 'm__': 103, 'n': 104, 'n^.': 105, 'n__': 106, 'o': 107, 'o^.': 108, 'o^^': 109, 'p': 110, 'p^.': 111, 'q': 112, 'qua': 113, 'r': 114, 'r^.': 115, 'r__': 116, 's': 117, 's^.': 118, 'sci': 119, 't': 120, 'u': 121, 'u^^': 122, 'u__': 123, 'v': 124, 'w': 125, 'x': 126, 'x^.': 127, 'y': 128, 'y^..': 129, 'z': 130, '{': 131, '}': 132}
    index2vocab = {0: '<BLANK>', 1: '<GO>', 2: '<STOP>', 3: '<PAD>', 4: ' ', 5: '"', 6: '%%', 7: '%%%', 8: '%%%%%', 9: '(', 10: '(:', 11: ')', 12: '*krussedull*', 13: '+', 14: '.', 15: '..', 16: '...', 17: '3', 18: ':', 19: ':)', 20: '=', 21: '@', 22: 'Alkali', 23: 'BallotScriptX', 24: 'BigB', 25: 'BigC', 26: 'BigD', 27: 'BigF', 28: 'BigFire', 29: 'BigG', 30: 'BigH', 31: 'BigInsularD', 32: 'BigJ', 33: 'BigK', 34: 'BigL', 35: 'BigM', 36: 'BigN', 37: 'BigP', 38: 'BigQ', 39: 'BigR', 40: 'BigS', 41: 'BigT', 42: 'BigV', 43: 'BigW', 44: 'BigZ', 45: 'CapitalGamma', 46: 'CapitalLambda', 47: 'CircledEquals', 48: 'Cloud', 49: 'Dagger', 50: 'Dissolve', 51: 'Dissolve_Square', 52: 'Earth', 53: 'Eye', 54: 'Female', 55: 'Fire', 56: 'Infinity', 57: 'InsularD', 58: 'Integral', 59: 'LatinLongLigatureFi', 60: 'LatinSmallLigatureFi', 61: 'NorthEastArrow', 62: 'NotEqualTo', 63: 'Pentagram', 64: 'PhoenicianLetterPe', 65: 'PlainBigL', 66: 'RockSalt', 67: 'Saturn', 68: 'ScriptSmallG', 69: 'ScriptSmallZ', 70: 'SleepingSymbol', 71: 'SmallDelta', 72: 'SmallIota', 73: 'SmallNHook', 74: 'SmallPi', 75: 'SquareP', 76: 'SquaredPlus', 77: 'SquaredRisingDiagonalSlash', 78: 'TopHalfIntegral', 79: 'TriangleDot', 80: 'UpwardsArrow', 81: 'VerticalLine', 82: 'a', 83: 'a^^', 84: 'b', 85: 'c', 86: 'c^.', 87: 'd', 88: 'e', 89: 'e?', 90: 'e^^', 91: 'f', 92: 'g', 93: 'gate', 94: 'h', 95: 'h^.', 96: 'i', 97: 'i^^', 98: 'j', 99: 'k', 100: 'l', 101: 'm', 102: 'm^.', 103: 'm__', 104: 'n', 105: 'n^.', 106: 'n__', 107: 'o', 108: 'o^.', 109: 'o^^', 110: 'p', 111: 'p^.', 112: 'q', 113: 'qua', 114: 'r', 115: 'r^.', 116: 'r__', 117: 's', 118: 's^.', 119: 'sci', 120: 't', 121: 'u', 122: 'u^^', 123: 'u__', 124: 'v', 125: 'w', 126: 'x', 127: 'x^.', 128: 'y', 129: 'y^..', 130: 'z', 131: '{', 132: '}'}
    
    prediction = preds_ex3
    
    predsAStr = decodePred(prediction, "")
    predsBStr = decodePred(prediction, "@")
    predsCStr = decodePred(prediction, "<ERROR>")
    gtStr = decode(gt)
    
    cer = CharErrorRate()
    
    cerA = cer(" ".join(predsAStr), " ".join(gtStr)).item()
    cerB = cer(" ".join(predsBStr), " ".join(gtStr)).item()
    cerC = cer(" ".join(predsCStr), " ".join(gtStr)).item()
    
    levA = levenshtein(prediction, gt)[0]
    
    metrics = [cerA, cerB, cerC, levA]
    print(metrics)
    
    ###########################################################################
    
    lens = []
    for word in vocab:
        lens.append(len(word))

    
    data = ['3.459930419921875', '19.18181800842285', '4.349264621734619', '2614.0', '8.0', '11.368888854980469']
    data = np.array(data, dtype=float)
    
    print(data[0])
    print(type(data[0]))
    print("")
    print(data[5])
    print(type(data[5]))
    
    
    
    
    