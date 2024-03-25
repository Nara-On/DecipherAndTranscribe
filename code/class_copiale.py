# -*- coding: utf-8 -*-

from PIL import ImageFont, ImageDraw, Image, ImageOps
from collections import defaultdict
import os


class Copiale:
    
    def __init__(self, num_lines):
        
        self.translator = self.createDict()
        self.num_files = num_lines
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`^~0123456789.:,!?/\\"%^&-+@#<>){}[]=|_*;($\' '
    
    
    def createDict(self):
        
        # Dictionary with default values
        translator = defaultdict(lambda: '')
        
        # Letters
        translator['a'] = 'a'
        translator['a^^'] = 'A'
        translator['BigA'] = 'a' # No direct translation
        translator['b'] = 'b'
        translator['BigB'] = 'b' # No direct translation
        translator['c'] = 'c'
        translator['c^.'] = 'C'
        translator['BigC'] = 'c' # No direct translation
        translator['d'] = 'd'
        translator['BigD'] = 'd' # No direct translation
        translator['e'] = 'e'
        translator['e^^'] = 'E'
        translator['BigE'] = 'e' # No direct translation
        translator['f'] = 'f'
        translator['BigF'] = '_' # More or less
        translator['g'] = 'g'
        translator['BigG'] = 'g' # No direct translation
        translator['h'] = 'h'
        translator['h^.'] = 'H'
        translator['BigH'] = 'h' # No direct translation
        translator['i'] = 'i'
        translator['i^^'] = 'I'
        translator['BigI'] = 'i' # No direct translation
        translator['j'] = 'j'
        translator['BigJ'] = 'j' # No direct translation
        translator['k'] = 'k'
        translator['BigK'] = 'k' # No direct translation
        translator['l'] = 'l'
        translator['BigL'] = 'l' # No direct translation
        translator['m'] = 'm'
        translator['m^.'] = 'M'
        translator['m__'] = 'B'
        translator['BigM'] = 'm' # No direct translation
        translator['n'] = 'n'
        translator['n^.'] = 'N'
        translator['n__'] = 'D'
        translator['BigN'] = 'n' # No direct translation
        translator['o'] = 'o'
        translator['o^.'] = '&'
        translator['o^^'] = 'O'
        translator['BigO'] = 'o' # No direct translation
        translator['p'] = 'p'
        translator['p^.'] = 'P'
        translator['BigP'] = 'p' # No direct translation
        translator['q'] = 'q'
        translator['BigQ'] = 'q' # No direct translation
        translator['r'] = 'r'
        translator['r^.'] = 'R'
        translator['r__'] = 'F'
        translator['BigR'] = 'r' # No direct translation
        translator['s'] = 's'
        translator['s^.'] = 'S'
        translator['BigS'] = 's' # No direct translation
        translator['t'] = 't'
        translator['BigT'] = 't' # No direct translation
        translator['u'] = 'u'
        translator['u^^'] = 'U'
        translator['u__'] = 'G'
        translator['BigU'] = 'u' # No direct translation
        translator['v'] = 'v'
        translator['BigV'] = 'v' # No direct translation
        translator['w'] = 'w'
        translator['BigW'] = 'w' # No direct translation
        translator['x'] = 'x'
        translator['x^.'] = 'X'
        translator['BigX'] = 'x' # No direct translation
        translator['y^..'] = 'y'
        translator['BigY'] = 'y' # No direct translation
        translator['z'] = 'z'
        translator['BigZ'] = 'z' # No direct translation
        
        # Symbols
        translator['+'] = '+'
        translator['.'] = '.'
        translator['..'] = '..'
        translator['...'] = ','
        translator[':'] = ':'
        translator['='] = '='
        translator['3'] = '3'
        
        # Logograms
        translator['Alkali'] = '9'
        translator['BallotScriptX'] = '%'
        translator['BigFire'] = '<' # No direct translation
        translator['BigInsularD'] = 'L' # No direct translation
        translator['CapitalGamma'] = '~'
        translator['CapitalLambda'] = '^'
        translator['CircledEquals'] = '@'
        translator['Dagger'] = 'T'
        translator['Earth'] = '1'
        translator['Eye'] = '2'
        translator['Female'] = '0'
        translator['Fire'] = '<'
        translator['Infinity'] = '8'
        translator['InsularD'] = 'L'
        translator['Integral'] = '`'
        translator['LatinLongLigatureFi'] = ']'
        translator['LatinSmallLigatureFi'] = ')'
        translator['NorthEastArrow'] = "/"
        translator['NotEqualTo'] = '"'
        translator['PhoenicianLetterPe'] = '?'
        translator['RockSalt'] = '5'
        translator['Saturn'] = '-'
        translator['ScriptSmallG'] = 'K'
        translator['ScriptSmallZ'] = 'J'
        translator['SleepingSymbol'] = 'Z'
        translator['SmallDelta'] = '6'
        translator['SmallIota'] = '!' 
        translator['SmallNHook'] = 'Y'
        translator['SmallPi'] = '>'
        translator['SquareP'] = 'Q'
        translator['SquaredPlus'] = '['
        translator['SquaredRisingDiagonalSlash'] = 'W'
        translator['TopHalfIntegral'] = '7'
        translator['TriangleDot'] = '#'
        translator['UpwardsArrow'] = '4'
        translator['VerticalLine'] = '|'
        
        # Copiale V2
        translator['(:'] = '('
        translator[':)'] = '$'
        translator['gate'] = '\''
        translator['Cloud'] = ';'
        translator['Pentagram'] = '*'
        
        # Not found in trainset, in font
        translator['TF'] = '\\'
        
        # Corrections
        translator['e?'] = '3' # Assumed wrong direction
        translator['qua'] = 'W' # Assumed missing line
        translator['('] = '(' # Assumed missing points
        translator[')'] = '$' # Assumed missing points
        
        return translator
        
        
    def transcr2font(self, message):
        
        msg = message.split(" ")
        translation = ""
            
        for c in msg:
            translation += self.translator[c]
        return translation
            
            
    def gen_realLines(self, savepath):
        """
        Generator of syntheticimages from a real-life example
        
        """
        
        image_savepath = savepath + "sint/images/"
        groundtruth_savepath = savepath + "sint/groundtruth/"
        
        # Generate directories if necessary
        if not os.path.exists(image_savepath):
            os.makedirs(image_savepath)
        if not os.path.exists(groundtruth_savepath):
            os.makedirs(groundtruth_savepath)
            
        # Read cipher file
        font = ImageFont.truetype("../ciphers/CopialeV2.ttf", size=120)
        
        for i in range(0, self.num_files, 1):
                
            # Read groundtruth from the real images
            file = "../databases/copiale_real-vs-sint/real/groundtruth/T2_" + str(i).rjust(4, '0') + ".txt"
            
            t2 = open(file, "r", encoding="UTF-8")
            line = self.transcr2font(t2.read())
            t2.close()

            # Create background image
            im = Image.new('L', size=(50,50), color=255)
            scratch_draw = ImageDraw.Draw(im)
            
            # Calculate size text
            textsize = scratch_draw.multiline_textsize(line, font=font, spacing=0)
            padding = (50, 50)  # Adjust padding as needed
            textsize = (textsize[0] + padding[0], textsize[1] + padding[1])
            
            # Create final image
            im = Image.new('L', textsize,)
            draw = ImageDraw.Draw(im)
            
            start_position = ((padding[0]) // 2, 0)
            draw.multiline_text(xy=start_position, text=line, fill=255, font=font, spacing=0, align="center")

            # Border
            im = ImageOps.invert(im)
            im = ImageOps.expand(im, border=(20, 10, 20, 10), fill="white")
            im.save(image_savepath + "t2_" + str(i).rjust(4, '0') + ".png","PNG")
                
            f = open(groundtruth_savepath + "t2_" + str(i).rjust(4, '0') + ".txt","w")
            f.write(line)
            f.close()       

            
    def print_alphabet(self):
        
        for i,c in enumerate(self.alphabet):
            print(str(i) + ": " + c)
            
            # Create savepath routes
            savepath = "../databases/copiale_alphabet/"
            
            # Generate directories if necessary
            if not os.path.exists(savepath):
                os.makedirs(savepath)
                
            # Read cipher file
            font = ImageFont.truetype("../ciphers/CopialeV2.ttf", size=120)
            
            # Create background image
            im = Image.new('L', size=(50,50), color=255)
            scratch_draw = ImageDraw.Draw(im)
            
            # Calculate size text
            textsize = scratch_draw.multiline_textsize(c, font=font, spacing=0)
            padding = (50, 50)  # Adjust padding as needed
            textsize = (textsize[0] + padding[0], textsize[1] + padding[1])
            
            # Create final image
            im = Image.new('L', textsize,)
            draw = ImageDraw.Draw(im)
            
            start_position = ((padding[0]) // 2, 0)
            draw.multiline_text(xy=start_position, text=c, fill=255, font=font, spacing=0, align="center")

            # Border
            im = ImageOps.invert(im)
            im = ImageOps.expand(im, border=(2, 2, 2, 2), fill="white")
            
            im.save(savepath + "copialeV2_" + str(i) + ".png","PNG")
            
            