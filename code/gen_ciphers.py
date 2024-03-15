# -*- coding: utf-8 -*-

from PIL import ImageFont, ImageDraw, Image, ImageOps

import random
import os


ttfs = ["Masonic_Cipher.ttf","KeilFont.ttf","Stickman.ttf", 
        "Copiale.ttf","ModernRunic-Regular.ttf", "PigpenCipher.otf"]

files = ["big_LittleWomen.txt", "big_AlicesAdventuresInWonderland.txt", "big_Lazarillo.txt", "big_Quijote.txt"]
lines = ["quotes.txt"]

alphabet_default = "abcdefghijklmnopqrstuvwxyz "
alphabet_copiale = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.:,!?/\\")%^&-+@~#<>{}[]=|_ '
alphabet_numerical = "0123456789 "

# Gen lines rand
min_num_chars = 20
max_num_chars = 40
num_lines = 10

# Gen texts
num_chars = 25 # per image


def gen_lines_rand(ttfs):
    
    for ttf in ttfs:
    	image_savepath = "../databases/lines/" + ttf.split(".")[0].lower() + "/images/"
    	groundtruth_savepath = "../databases/lines/" + ttf.split(".")[0].lower() + "/groundtruth/"
        
    	if not os.path.exists(image_savepath):
    		os.makedirs(image_savepath)
    	if not os.path.exists(groundtruth_savepath):
    		os.makedirs(groundtruth_savepath)
        
    	border = (20, 10, 20, 10)
    	
    	if ttf.split(".")[0].lower() == "copiale":
            selected_alphabet = alphabet_copiale
    	else:
            selected_alphabet = alphabet_default
            
    	font = ImageFont.truetype("../ciphers/" + ttf, size=120)
        
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
        image_savepath = "../databases/lines/" + ttf.split(".")[0].lower() + "/images/"
        groundtruth_savepath = "../databases/lines/" + ttf.split(".")[0].lower() + "/groundtruth/"
           
        if not os.path.exists(image_savepath):
       		os.makedirs(image_savepath)
        if not os.path.exists(groundtruth_savepath):
       		os.makedirs(groundtruth_savepath)
           
        border = (20, 10, 20, 10)
       	
        selected_alphabet = alphabet_numerical
               
        font = ImageFont.truetype("../ciphers/Copiale.ttf", size=120)   
                
        props = [5]*len(selected_alphabet)
        props[-1] = 15
        
        index = 0
        
        for file in files:
            l = open("../texts/" + file, "r")
            
            im = Image.new('L',(1,1), color=255)
            scratch_draw = ImageDraw.Draw(im)
            
            for text in l.readlines():
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
                   index = index+1
            l.close()
                
           
def gen_lines_nums():
    
    image_savepath = "../databases/nums/images/"
    groundtruth_savepath = "../databases/nums/groundtruth/"
       
    if not os.path.exists(image_savepath):
   		os.makedirs(image_savepath)
    if not os.path.exists(groundtruth_savepath):
   		os.makedirs(groundtruth_savepath)
       
    border = (20, 10, 20, 10)
   	
    selected_alphabet = alphabet_numerical
           
    font = ImageFont.truetype("../ciphers/Copiale.ttf", size=120)
       
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
           im.save(image_savepath + "copiale_" + str(index) + ".png","PNG")
           
           f = open(groundtruth_savepath + "copiale_"+str(index) + ".txt","w")
           f.write(text)
           f.close()
            
            
def gen_txt(ttfs, files):
    
    for ttf in ttfs:
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
                draw.multiline_text(xy=(0,0), text=text,fill=255, font=font, spacing=40)
                im = ImageOps.invert(im)
                im.save(image_savepath + ttf.split(".")[0].lower() + "_" + str(index) + ".png","PNG")
        
                f = open(groundtruth_savepath + ttf.split(".")[0].lower() + "_" + str(index) + ".txt","w")
                f.write(text)
                f.close()
                index = index+1




###########################################################################################################

def gen_single_lines(ttf, text):
    
    savepath = "../databases/trials/lines/"
        
    if not os.path.exists(savepath):
   		os.makedirs(savepath)
       
    border = (20, 10, 20, 10)
   	
    if ttf.split(".")[0].lower() == "copiale":
           selected_alphabet = alphabet_copiale
    else:
           selected_alphabet = alphabet_default
           
    font = ImageFont.truetype("../ciphers/" + ttf, size=120)
       
    props = [5]*len(selected_alphabet)
    props[-1] = 15
   
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
    
    image_savepath = "../databases/trials/texts/"
       
    if not os.path.exists(image_savepath):
   		os.makedirs(image_savepath)
           
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

    im = Image.new('L',(1,1), color=255)
    scratch_draw = ImageDraw.Draw(im)
    for index,text in enumerate(pack):
   		textsize = scratch_draw.multiline_textsize(text, font=font, spacing=40)
   		
   		im = Image.new('L',textsize,)
   		draw = ImageDraw.Draw(im)
   		draw.multiline_text(xy=(0,0), text=text,fill=255, font=font, spacing=40)
   		im = ImageOps.invert(im)
   		im.save(image_savepath + ttf.split(".")[0].lower() + "_"+str(index) + ".png","PNG")

   		f = open(image_savepath + ttf.split(".")[0].lower() + "_"+str(index) + ".txt","w")
   		f.write(text)
   		f.close()
                
###########################################################################################################


if __name__ == '__main__':
    
	#gen_lines(ttfs, lines)
    #gen_lines_rand(ttfs)
    #gen_lines_nums()
    #gen_txt(ttfs, files)
    
    """
    for ttf in ttfs:
        gen_single_lines(ttf, "hello world")
        gen_single_txt(ttf, "mid_Ozymandias.txt")
    """    