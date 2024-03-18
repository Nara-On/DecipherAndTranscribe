# -*- coding: utf-8 -*-

from PIL import ImageFont, ImageDraw, Image, ImageOps

import os
import random
import warnings

warnings.filterwarnings("ignore", category = DeprecationWarning) 


# Files
ttfs = ["Masonic_Cipher.ttf","KeilFont.ttf","Stickman.ttf", 
        "Copiale.ttf","ModernRunic-Regular.ttf", "PigpenCipher.otf"]

lines = ["quotes.txt"]
texts = ["chapters_LittleWomen.txt", "chapters_AliceInWonderland.txt", 
         "chapters_Lazarillo.txt", "chapters_Quijote.txt"]

# Alphabets
alphabet_numerical = "0123456789 "
alphabet_default = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '

alphabet_copiale = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.:,!?/\\")%^&-+@~#<>{}[]=|_ '
alphabet_keilfont = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.:,!?/\\")%&-+@~#<>{}=|_ '
alphabet_masonic = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.:, '
alphabet_runic = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz:,!?/\\"#{}[] '
alphabet_stickman = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.," '
alphabet_pigpen = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.:," '

alphabets = [alphabet_masonic, alphabet_keilfont, alphabet_stickman, 
             alphabet_copiale, alphabet_runic, alphabet_pigpen]

# Gen lines rand + num
min_num_chars = 20
max_num_chars = 40

# Gen texts
num_chars = 20 # per image



def gen_lines_rand(ttfs, num_lines):
    """
    Generator of randomized lines
    
    Inputs: 
        - ttfs = Cipher files
        - num_linies = Number of generated lines
    
    """
    for ttf in ttfs:
        print("Generating random lines from " + ttf.split(".")[0].lower() + "...")
        # Create savepath routes
        image_savepath = "../databases/lines/" + ttf.split(".")[0].lower() + "/images/"
        groundtruth_savepath = "../databases/lines/" + ttf.split(".")[0].lower() + "/groundtruth/"
        
        # Generate directories if necessary
        if not os.path.exists(image_savepath):
            os.makedirs(image_savepath)
        if not os.path.exists(groundtruth_savepath):
            os.makedirs(groundtruth_savepath)
            
        # Read cipher file
        font = ImageFont.truetype("../ciphers/" + ttf, size=120)
        
        # Choose an alphabet
        if ttf.split(".")[0].lower() == "copiale":
            selected_alphabet = alphabet_copiale
        else:
            selected_alphabet = alphabet_default
        
        # Parameters for the generation of randomized lines
        border = (20, 10, 20, 10)
        props = [5]*len(selected_alphabet)
        props[-1] = 15
        pack = []
        
        # Generate randomized lines
        while len(pack) <= num_lines:
            pack.append(''.join(random.choices(selected_alphabet, weights=props)[0] for i in range(random.randint(min_num_chars, max_num_chars)))+"\n")
            
        # Create background image
        im = Image.new('L',(1,1), color=255)
        scratch_draw = ImageDraw.Draw(im)
        
        # Copy text into the background image
        for index,text in enumerate(pack):
            textsize = scratch_draw.multiline_textsize(text, font=font, spacing=-10)
            
            im = Image.new('L', textsize,)
            draw = ImageDraw.Draw(im)
            draw.multiline_text(xy=(0,0), text=text, fill=255, font=font, spacing=-10)
            im = ImageOps.invert(im)
            im = ImageOps.expand(im, border=border, fill="white")
            im.save(image_savepath + ttf.split(".")[0].lower() + "_" + str(index) + ".png","PNG")
            
            f = open(groundtruth_savepath + ttf.split(".")[0].lower() + "_"+str(index) + ".txt","w")
            f.write(text)
            f.close()


def gen_lines_nums(num_lines):
    """
    Generator of randomized numeric lines
    
    Inputs: 
        - num_linies = Number of generated lines
    
    """
    print("Generating numeric lines from copiale...")
    
    # Create savepath routes
    image_savepath = "../databases/nums/images/"
    groundtruth_savepath = "../databases/nums/groundtruth/"
    
    # Generate directories if necessary
    if not os.path.exists(image_savepath):
        os.makedirs(image_savepath)
    if not os.path.exists(groundtruth_savepath):
        os.makedirs(groundtruth_savepath)
        
    # Read cipher file
    font = ImageFont.truetype("../ciphers/Copiale.ttf", size=120)
    
    # Parameters for the generation of randomized lines
    border = (20, 10, 20, 10)
    props = [5]*len(alphabet_numerical)
    props[-1] = 15   
    pack = []
    
    # Generate randomized lines
    while len(pack) <= num_lines:
        pack.append(''.join(random.choices(alphabet_numerical, weights=props)[0] for i in range(random.randint(min_num_chars, max_num_chars)))+"\n")
        
    # Create background image
    im = Image.new('L',(1,1), color=255)
    scratch_draw = ImageDraw.Draw(im)
    
    # Copy text into the background image
    for index,text in enumerate(pack):
        textsize = scratch_draw.multiline_textsize(text, font=font, spacing=-10)
        
        im = Image.new('L', textsize,)
        draw = ImageDraw.Draw(im)
        draw.multiline_text(xy=(0,0), text=text, fill=255, font=font, spacing=-10)
        im = ImageOps.invert(im)
        im = ImageOps.expand(im, border=border, fill="white")
        im.save(image_savepath + "copiale_" + str(index) + ".png","PNG")
        
        f = open(groundtruth_savepath + "copiale_"+str(index) + ".txt","w")
        f.write(text)
        f.close()


def gen_lines(ttfs, files):
    """
    Generator of lines from txt files
    
    Inputs: 
        - ttfs = Cipher files
        - files = Text files
    
    """
    for ttf in ttfs:
        print("Generating lines from " + ttf.split(".")[0].lower() + "...")
        
        # Create savepath routes
        image_savepath = "../databases/lines/" + ttf.split(".")[0].lower() + "/images/"
        groundtruth_savepath = "../databases/lines/" + ttf.split(".")[0].lower() + "/groundtruth/"
        
        # Generate directories if necessary
        if not os.path.exists(image_savepath):
            os.makedirs(image_savepath)
        if not os.path.exists(groundtruth_savepath):
            os.makedirs(groundtruth_savepath)
            
        # Read cipher file
        font = ImageFont.truetype("../ciphers/" + ttf, size=120)
        
        # Parameters for the generation of randomized lines
        border = (20, 10, 20, 10)
        index = 0
        
        for file_char in files:
            print("- File " + file_char.split(".")[0].lower())
            
            # Read text file
            l = open("../texts/" + file_char, "r")
            
            # Create background image
            im = Image.new('L',(1,1), color=255)
            scratch_draw = ImageDraw.Draw(im)
            
            # Copy text into the background image
            for txt in l.readlines():
                text = txt.strip()
                textsize = scratch_draw.multiline_textsize(text, font=font, spacing=-10)
                
                im = Image.new('L', textsize,)
                draw = ImageDraw.Draw(im)
                draw.multiline_text(xy=(0,0), text=text, fill=255, font=font, spacing=-10)
                im = ImageOps.invert(im)
                im = ImageOps.expand(im, border=border, fill="white")
                im.save(image_savepath + ttf.split(".")[0].lower() + "_" + str(index) + ".png","PNG")
                
                f = open(groundtruth_savepath + ttf.split(".")[0].lower() + "_" + str(index) + ".txt","w")
                f.write(text)
                f.close()
                index += 1
            l.close()
            
            
def gen_txt(ttfs, files):
    """
    Generator of text images from txt files
    
    Inputs: 
        - ttfs = Cipher files
        - files = Text files
    
    """
    for ttf in ttfs:
        print("Generating text from " + ttf.split(".")[0].lower() + "...")
        
        # Create savepath routes
        image_savepath = "../databases/texts/" + ttf.split(".")[0].lower() + "/images/"
        groundtruth_savepath = "../databases/texts/" + ttf.split(".")[0].lower() + "/groundtruth/"
        
        # Generate directories if necessary
        if not os.path.exists(image_savepath):
            os.makedirs(image_savepath)
        if not os.path.exists(groundtruth_savepath):
            os.makedirs(groundtruth_savepath)
            
        # Read cipher file
        font = ImageFont.truetype("../ciphers/" + ttf, size=120)
        
        # Choose an alphabet
        if ttf.split(".")[0].lower() == "copiale":
            selected_alphabet = alphabet_copiale
        else:
            selected_alphabet = alphabet_default
        
        # Image index
        index = 0
        
        for file_char in files:
            print("- File " + file_char.split(".")[0].lower())
            
            # Read text file
            file = open("../texts/" + file_char, "r", encoding="UTF-8")
            
            # Filter characters
            big_text = ""
            for line in file:
                line = line.rstrip()
                line = line.lower()
                filtered = ""
                for c in line:
                    if c in selected_alphabet:
                        filtered += c
                    big_text += filtered
                    
            # Justify text
            pack = []
            justified_text = " "
            countChar = 0
            countLine = 0
            for c in big_text:
                justified_text += c
                countChar += 1
                if countChar < num_chars:
                    justified_text += " "
                else:
                    countChar = 0
                    countLine += 1
                    if countLine < num_chars:
                        justified_text += " \n "
                    else:
                        countLine = 0
                        pack.append(justified_text)
                        justified_text = " "
                        
            # Create background image
            im = Image.new('L',(1,1), color=255)
            scratch_draw = ImageDraw.Draw(im)
            
            # Copy text into the background image
            for text in pack:
                textsize = scratch_draw.multiline_textsize(text, font=font, spacing=40)
                
                im = Image.new('L',textsize,)
                draw = ImageDraw.Draw(im)
                draw.multiline_text(xy=(0,8), text=text, fill=255, font=font, spacing=38)
                im = ImageOps.invert(im)
                im.save(image_savepath + ttf.split(".")[0].lower() + "_" + str(index) + ".png","PNG")
                
                f = open(groundtruth_savepath + ttf.split(".")[0].lower() + "_" + str(index) + ".txt","w")
                f.write(text)
                f.close()
                index += 1


def gen_single_lines(ttf, text):
    """
    Generator of lines from a txt file
    
    Inputs: 
        - ttfs = Cipher files
        - text = Text file
    
    """
    # Create savepath routes
    savepath = "../databases/trials/lines/"
    
    # Generate directories if necessary
    if not os.path.exists(savepath):
        os.makedirs(savepath)
        
    # Read cipher file
    font = ImageFont.truetype("../ciphers/" + ttf, size=120)
    
    border = (20, 10, 20, 10)
    
    # Create background image
    im = Image.new('L',(1,1), color=255)
    scratch_draw = ImageDraw.Draw(im)
    
    # Copy text into the background image
    textsize = scratch_draw.multiline_textsize(text, font=font, spacing=-10)
    im = Image.new('L', textsize,)
    
    draw = ImageDraw.Draw(im)
    draw.multiline_text(xy=(0,0), text=text, fill=255, font=font, spacing=-10)
    im = ImageOps.invert(im)
    im = ImageOps.expand(im, border=border, fill="white")
    im.save(savepath + ttf.split(".")[0].lower() + ".png","PNG")
    
    f = open(savepath + ttf.split(".")[0].lower() + ".txt","w")
    f.write(text)
    f.close()
        

def gen_single_txt(ttf, file):
    """
    Generator of text images from a txt file
    
    Inputs: 
        - ttfs = Cipher files
        - file = Text file
    
    """
    # Create savepath routes
    savepath = "../databases/trials/texts/"
    
    # Generate directories if necessary
    if not os.path.exists(savepath):
        os.makedirs(savepath)
        
    # Read cipher file
    font = ImageFont.truetype("../ciphers/" + ttf, size=120)
    
    # Choose an alphabet
    if ttf.split(".")[0].lower() == "copiale":
        selected_alphabet = alphabet_copiale
    else:
        selected_alphabet = alphabet_default
        
    # Read text file
    file = open("../texts/" + file, "r", encoding="UTF-8")
    
    # Filter characters
    big_text = ""
    for line in file:
        line = line.rstrip()
        line = line.lower()
        filtered = ""
        for c in line:
            if c in selected_alphabet:
                filtered += c
            big_text += filtered
    
    # Justify text
    pack = []
    justified_text = " "
    countChar = 0
    countLine = 0
    for c in big_text:
        justified_text += c
        countChar += 1
        if countChar < num_chars:
            justified_text += " "
        else:
            countChar = 0
            countLine += 1
            if countLine < num_chars:
                justified_text += " \n "
            else:
                countLine = 0
                pack.append(justified_text)
                justified_text = " "
    
    # If text is too short, append it anyway
    if len(pack) == 0:
        pack.append(justified_text)
        
    # Create background image
    im = Image.new('L',(1,1), color=255)
    scratch_draw = ImageDraw.Draw(im)
    
    # Copy text into the background image
    for text in pack:
        textsize = scratch_draw.multiline_textsize(text, font=font, spacing=40)
        
        im = Image.new('L',textsize,)
        draw = ImageDraw.Draw(im)
        draw.multiline_text(xy=(0,8), text=text, fill=255, font=font, spacing=38)
        im = ImageOps.invert(im)
        im.save(savepath + ttf.split(".")[0].lower() + ".png","PNG")
        
        f = open(savepath + ttf.split(".")[0].lower() + ".txt","w")
        f.write(text)
        f.close()
                
           
###########################################################################################################

if __name__ == '__main__':
    
    num_lines = 200
    
    gen_lines(ttfs, lines)
    gen_lines_nums(num_lines)
    gen_txt(ttfs, texts)
    
    for ttf, alph in zip(ttfs, alphabets):
        gen_single_lines(ttf, alph)
        gen_single_txt(ttf, "mid_Ozymandias.txt")
        