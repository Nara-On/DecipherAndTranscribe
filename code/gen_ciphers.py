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


###########################################################################################################

def gen_lines_rand(ttfs, num_lines):
    
    for ttf in ttfs:
    	print("Generating random lines from " + ttf.split(".")[0].lower() + "...")
        
    	image_savepath = "../databases/lines/" + ttf.split(".")[0].lower() + "/images/"
    	groundtruth_savepath = "../databases/lines/" + ttf.split(".")[0].lower() + "/groundtruth/"
        
    	if not os.path.exists(image_savepath):
    		os.makedirs(image_savepath)
    	if not os.path.exists(groundtruth_savepath):
    		os.makedirs(groundtruth_savepath)
        
    	border = (20, 10, 20, 10)
    	font = ImageFont.truetype("../ciphers/" + ttf, size=120)
        
    	if ttf.split(".")[0].lower() == "copiale":
            selected_alphabet = alphabet_copiale
    	else:
            selected_alphabet = alphabet_default
        
    	props = [5]*len(selected_alphabet)
    	props[-1] = 15
        
    	pack = []
    
    	while len(pack) <= num_lines:
            pack.append(''.join(random.choices(selected_alphabet, weights=props)[0] for i in range(random.randint(min_num_chars, max_num_chars)))+"\n")
    
    	im = Image.new('L',(1,1), color=255)
    	scratch_draw = ImageDraw.Draw(im)
        
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


def gen_lines(ttfs, files):
    
    for ttf in ttfs:
        print("Generating lines from " + ttf.split(".")[0].lower() + "...")
        
        image_savepath = "../databases/lines/" + ttf.split(".")[0].lower() + "/images/"
        groundtruth_savepath = "../databases/lines/" + ttf.split(".")[0].lower() + "/groundtruth/"
           
        if not os.path.exists(image_savepath):
       		os.makedirs(image_savepath)
        if not os.path.exists(groundtruth_savepath):
       		os.makedirs(groundtruth_savepath)
           
        border = (20, 10, 20, 10)
        font = ImageFont.truetype("../ciphers/" + ttf, size=120)   
        
        index = 0
        
        for file_char in files:
            print("- File " + file_char.split(".")[0].lower())
            
            l = open("../texts/" + file_char, "r")
            
            im = Image.new('L',(1,1), color=255)
            scratch_draw = ImageDraw.Draw(im)
            
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
                
           
def gen_lines_nums(num_lines):
    
    print("Generating numeric lines from copiale...")
    
    image_savepath = "../databases/nums/images/"
    groundtruth_savepath = "../databases/nums/groundtruth/"
       
    if not os.path.exists(image_savepath):
   		os.makedirs(image_savepath)
    if not os.path.exists(groundtruth_savepath):
   		os.makedirs(groundtruth_savepath)
       
    border = (20, 10, 20, 10)
    font = ImageFont.truetype("../ciphers/Copiale.ttf", size=120)
       
    props = [5]*len(alphabet_numerical)
    props[-1] = 15
       
    pack = []
   
    while len(pack) <= num_lines:
           pack.append(''.join(random.choices(alphabet_numerical, weights=props)[0] for i in range(random.randint(min_num_chars, max_num_chars)))+"\n")
   
    im = Image.new('L',(1,1), color=255)
    scratch_draw = ImageDraw.Draw(im)
    
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
            
            
def gen_txt(ttfs, files):
    
    for ttf in ttfs:
    	print("Generating text from " + ttf.split(".")[0].lower() + "...")
        
    	image_savepath = "../databases/texts/" + ttf.split(".")[0].lower() + "/images/"
    	groundtruth_savepath = "../databases/texts/" + ttf.split(".")[0].lower() + "/groundtruth/"
        
    	if not os.path.exists(image_savepath):
    		os.makedirs(image_savepath)
    	if not os.path.exists(groundtruth_savepath):
    		os.makedirs(groundtruth_savepath)
            
    	if ttf.split(".")[0].lower() == "copiale":
            selected_alphabet = alphabet_copiale
    	else:
            selected_alphabet = alphabet_default
            
    	font = ImageFont.truetype("../ciphers/" + ttf, size=120)
    	index = 0
        
    	for file_char in files:
            print("- File " + file_char.split(".")[0].lower())
            
            file = open("../texts/" + file_char, "r", encoding="UTF-8")
               
            big_text = ""
            for line in file:
           		line = line.rstrip()
           		line = line.lower()
           		filtered = ""
           		for c in line:
           			if c in selected_alphabet:
           				filtered += c
           		big_text += filtered
        
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
        
            im = Image.new('L',(1,1), color=255)
            scratch_draw = ImageDraw.Draw(im)
            
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



###########################################################################################################

def gen_single_lines(ttf, text):
    
    savepath = "../databases/trials/lines/"
        
    if not os.path.exists(savepath):
        os.makedirs(savepath)
       
    border = (20, 10, 20, 10)       
    font = ImageFont.truetype("../ciphers/" + ttf, size=120)
   
    im = Image.new('L',(1,1), color=255)
    scratch_draw = ImageDraw.Draw(im)
    
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
    
    savepath = "../databases/trials/texts/"
       
    if not os.path.exists(savepath):
   		os.makedirs(savepath)
           
    if ttf.split(".")[0].lower() == "copiale":
        selected_alphabet = alphabet_copiale
    else:
        selected_alphabet = alphabet_default
           
    font = ImageFont.truetype("../ciphers/" + ttf, size=120)
    file = open("../texts/" + file, "r", encoding="UTF-8")
       
    big_text = ""
    for line in file:
   		line = line.rstrip()
   		line = line.lower()
   		filtered = ""
   		for c in line:
   			if c in selected_alphabet:
   				filtered += c
   		big_text += filtered

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
                   
    if len(pack) == 0:
        pack.append(justified_text)
        
    im = Image.new('L',(1,1), color=255)
    scratch_draw = ImageDraw.Draw(im)
    
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
        