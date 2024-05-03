# -*- coding: utf-8 -*-

from PIL import ImageFont, ImageDraw, Image, ImageOps
from difflib import get_close_matches
from collections import defaultdict

import numpy as np
import json
import os

import cv2
import random
from matplotlib import pyplot as plt


def gen_single_lines(ttf, c, i):
    """
    Generator of lines from a txt file
    
    Inputs: 
        - ttfs = Cipher files
        - text = Text file
    
    """
    # Create savepath routes
    savepath = "../databases/alphabet_test/"
    
    # Generate directories if necessary
    if not os.path.exists(savepath):
        os.makedirs(savepath)
        
    # Read cipher file
    font = ImageFont.truetype("../ciphers/" + ttf, size=120)
    
    # Create background image
    im = Image.new('L', size=(50,50), color=255)
    scratch_draw = ImageDraw.Draw(im)
    textsize = scratch_draw.multiline_textsize(c, font=font, spacing=0)
    
    padding = (50, 50)  # Adjust padding as needed
    textsize = (textsize[0] + padding[0], textsize[1] + padding[1])
    
    im = Image.new('L', textsize,)
    draw = ImageDraw.Draw(im)
    
    start_position = ((padding[0]) // 2, 0)
    draw.multiline_text(xy=start_position, text=c, fill=255, font=font, spacing=0, align="center")

    # Border
    im = ImageOps.invert(im)
    im = ImageOps.expand(im, border=(2, 2, 2, 2), fill="white")
    
    im.save(savepath + ttf.split(".")[0].lower() + "_" + str(i) + ".png","PNG")
    
    
def uniqueValues():
    """
    Generator of images from a real-life example
    
    """
    listChars = []
    
    for i in range(0,1502,1):
        
        # Missing 
        #if i==232 or i==315 or i==530 or i==554 or i==627 or i==785 or i==1335 or i==1480 or i==1777 or i==1865 or i==2391 or i==3395 or i==3856 or i==3883 or i==4159 or i==4169 or i==4307 or i==4330 or i==4439 or i==4616 or i==4693 or i==4738 or i==5214:
        #    continue
        
        # Read groundtruth from the real images
        #file_T1 = "../databases/real-vs-sint/real/groundtruth/T1_" + str(i).rjust(4, '0') + ".txt"
        file_T2 = "../../databases/copiale_real-vs-sint/real/groundtruth/T2_" + str(i).rjust(4, '0') + ".txt"
        
        #t1 = open(file_T1, "r", encoding="UTF-8")
        t2 = open(file_T2, "r", encoding="UTF-8")
        
        #lineT1 = t1.read()
        lineT2 = t2.read()
            
        #t1.close()
        t2.close()
        
        #listChars.extend(lineT1.split(" "))
        listChars.extend(lineT2.split(" "))
        
    return np.unique(listChars)


def getAllLines():
    file_tr = "../../databases/copiale_real-vs-sint/real/copiale-transcription.txt"
    file_de = "../../databases/copiale_real-vs-sint/real/copiale-deciphered.txt"
    
    tr = open(file_tr, "r", encoding="UTF-8")
    de = open(file_de, "r", encoding="UTF-8")
    
    text_tr = tr.read()
    text_de = de.read()
    
    list_tr = [t for t in text_tr.split("\n") if t.strip()]
    list_de = [d for d in text_de.split("\n") if d.strip()]
    
    
    # Dictionary with default values
    transcribe = defaultdict(lambda: '')
    
    # Letters
    transcribe['a'] = 'a'
    transcribe['ah'] = 'a^^'
    transcribe['A'] = 'BigA' 
    transcribe['b'] = 'b'
    transcribe['B'] = 'BigB' 
    transcribe['c'] = 'c'
    transcribe['c.'] = 'c^.'
    transcribe['C'] = 'BigC' 
    transcribe['d'] = 'd'
    transcribe['D'] = 'BigD' 
    transcribe['e'] = 'e'
    transcribe['eh'] = 'e^^'
    transcribe['E'] = 'BigE' 
    transcribe['f'] = 'f'
    transcribe['F'] = 'BigF' 
    transcribe['g'] = 'g'
    transcribe['G'] = 'BigG'
    transcribe['h'] = 'h'
    transcribe['h.'] = 'h^.'
    transcribe['H'] = 'BigH' 
    transcribe['i'] = 'i'
    transcribe['ih'] = 'i^^'
    transcribe['I'] = 'BigI' 
    transcribe['j'] = 'j'
    transcribe['J'] = 'BigJ' 
    transcribe['k'] = 'k'
    transcribe['K'] = 'BigK' 
    transcribe['l'] = 'l'
    transcribe['L'] = 'BigL'
    transcribe['m'] = 'm'
    transcribe['m.'] = 'm^.'
    transcribe['mu'] = 'm__'
    transcribe['M'] = 'BigM' 
    transcribe['n'] = 'n'
    transcribe['n.'] = 'n^.'
    transcribe['nu'] = 'n__'
    transcribe['N'] = 'BigN' 
    transcribe['o'] = 'o'
    transcribe['o.'] = 'o^.'
    transcribe['oh'] = 'o^^'
    transcribe['O'] = 'BigO'
    transcribe['p'] = 'p'
    transcribe['p.'] = 'p^.'
    transcribe['P'] = 'BigP' 
    transcribe['q'] = 'q'
    transcribe['Q'] = 'BigQ' 
    transcribe['r'] = 'r'
    transcribe['r.'] = 'r^.'
    transcribe['ru'] = 'r__'
    transcribe['R'] = 'BigR' 
    transcribe['s'] = 's'
    transcribe['s.'] = 's^.'
    transcribe['S'] = 'BigS' 
    transcribe['t'] = 't'
    transcribe['T'] = 'BigT' 
    transcribe['u'] = 'u'
    transcribe['uh'] = 'u^^'
    transcribe['uu'] = 'u__'
    transcribe['U'] = 'BigU'
    transcribe['v'] = 'v'
    transcribe['V'] = 'BigV'
    transcribe['w'] = 'w'
    transcribe['W'] = 'BigW' 
    transcribe['x'] = 'x'
    transcribe['x.'] = 'x^.'
    transcribe['X'] = 'BigX' 
    transcribe['y..'] = 'y^..'
    transcribe['Y'] = 'BigY' 
    transcribe['z'] = 'z'
    transcribe['Z'] = 'BigZ' 
    
    # Symbols
    transcribe['plus'] = '+'
    transcribe['.'] = '.'
    transcribe['..'] = '..' 
    transcribe['...'] = '...'
    transcribe[':'] = ':'
    transcribe['ni'] = '='
    transcribe['three'] = '3'
    transcribe['smil'] = '(:'
    transcribe['smir'] = ':)'
    transcribe['"'] = '"' 
    
    # Logograms
    transcribe['nee'] = 'Alkali'
    transcribe['bigx'] = 'BallotScriptX'
    transcribe['tribig'] = 'BigFire' 
    transcribe['DS'] = 'BigInsularD'
    transcribe['sqi'] = 'CapitalGamma'
    transcribe['lam'] = 'CapitalLambda'
    transcribe['o..'] = 'CircledEquals'
    transcribe['cross'] = 'Dagger'
    transcribe['mal'] = 'Earth'
    transcribe['lip'] = 'Eye'
    transcribe['fem'] = 'Female'
    transcribe['tri'] = 'Fire'
    transcribe['inf'] = 'Infinity'
    transcribe['ds'] = 'InsularD'
    transcribe['longs'] = 'Integral'
    transcribe['grl'] = 'LatinLongLigatureFi'
    transcribe['grr'] = 'LatinSmallLigatureFi'
    transcribe['arr'] = 'NorthEastArrow'
    transcribe['ki'] = 'NotEqualTo'
    transcribe['bas'] = 'PhoenicianLetterPe'
    transcribe['gam'] = 'RockSalt'
    transcribe['hd'] = 'Saturn'
    transcribe['gs'] = 'ScriptSmallG'
    transcribe['zs'] = 'ScriptSmallZ'
    transcribe['zzz'] = 'SleepingSymbol'
    transcribe['del'] = 'SmallDelta'
    transcribe['iot'] = 'SmallIota' 
    transcribe['ns'] = 'SmallNHook'
    transcribe['pi'] = 'SmallPi'
    transcribe['sqp'] = 'SquareP'
    transcribe['grc'] = 'SquaredPlus'
    transcribe['no'] = 'SquaredRisingDiagonalSlash'
    transcribe['hk'] = 'TopHalfIntegral'
    transcribe['tri..'] = 'TriangleDot'
    transcribe['car'] = 'UpwardsArrow'
    transcribe['bar'] = 'VerticalLine'
    transcribe['gate'] = 'gate'
    transcribe['toe'] = 'Cloud'
    transcribe['star'] = 'Pentagram'
    
    transcribe['ft'] = 'TF'
    
    transcribe['sci'] = 'sci'
    transcribe['qua'] = 'qua'
    transcribe[')'] = ')'
    transcribe['('] = '('
    transcribe['@'] = '@'
    transcribe['}'] = '}'
    transcribe['{'] = '{'
    transcribe['%%'] = '%%'
    transcribe['%%%'] = '%%%'
    transcribe['%%%%%'] = '%%%%'
    transcribe[')'] = ')'
    transcribe['e?'] = 'e?'
    transcribe[' '] = ' '
    transcribe['Dissolve'] = 'Dissolve'
    transcribe['*krussedull*'] = '*krussedull*'
    
    transcribe['PlainBigL'] = ''
    transcribe['pipe'] = 'F'
    
    return list_tr, list_de, transcribe
    

def transcr2tr(messageList, d):    
    tr = []
    for message in messageList:        
        msg = message.split(" ")
        translation = ""        
        for c in msg:
            translation += d[c]
            translation += " "
        tr.append(translation.strip())
    return tr


if __name__ == '__main__':
    
    u = uniqueValues()
    tr, de, di = getAllLines()
    tr2 = transcr2tr(tr, di)
    
    # Read values
    gt = []
    for text in os.listdir("../../databases/copiale_real-vs-sint/real/groundtruth"):
        file = "../../databases/copiale_real-vs-sint/real/groundtruth/" + text
        t = open(file, "r", encoding="UTF-8")
        gt.append(t.read())
        t.close()
    
    # Find index values TR2 - GT
    index = []
    foundGT = []
    for i, line in enumerate(gt):
        if line in tr2:
            index.append(tr2.index(line))
            foundGT.append(i)
        else:
            index.append("?")
    foundGT.sort()
    
    
    # Assign equal values
    assignedDe = list(np.zeros(len(gt)))
    for i in range(0, len(gt)):
        indTr = index[i]
        if indTr != "?":
            assignedDe[i] = de[indTr].strip()
    
    # Assign similar values by beginning
    stillMissing = []
    missing = [index for (index, item) in enumerate(assignedDe) if item == 0.0]
    
    for miss in missing:
        suggestions = [item for item in tr2 if item.startswith(gt[miss][0:40])]
        
        if len(suggestions) == 1:
            assignedDe[miss] = suggestions[0]
        else:
            stillMissing.append([miss, suggestions])
    
    # Assign similar values by ending
    manual = []
    for miss, i in stillMissing:
        suggestions = [item for item in tr2 if item.endswith(gt[miss][-40:])]
        
        if len(suggestions) == 1:
            assignedDe[miss] = suggestions[0]
        else:
            manual.append([miss, suggestions])
            
            
    # Export gt deciphered
    """
    if not os.path.exists("../databases/copiale_real-vs-sint/real/deciphered/"):
        os.makedirs("../databases/copiale_real-vs-sint/real/deciphered/")
            
    for i, dec in enumerate(assignedDe):
        f = open("../databases/copiale_real-vs-sint/real/deciphered/" + "d2_" + str(i).rjust(4, '0') + ".txt" ,"w")
        f.write(dec)
        f.close()   
    """
    