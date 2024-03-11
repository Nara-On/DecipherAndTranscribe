# -*- coding: utf-8 -*-

from PIL import ImageFont, ImageDraw, Image, ImageOps
import random
import shutil
import os


ttfs = ["Masonic_Cipher.ttf","KeilFont.ttf","Stickman.ttf", 
        "Copiale.ttf","ModernRunic-Regular.ttf", "PigpenCipher.otf"]

files = ["OFL.txt"]

alphabet_default = "abcdefghijklmnopqrstuvwxyz "
alphabet_copiale = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.:,!?/\\")%^&-+@~#<>{}[]=|_'

# Gen lines
min_num_chars = 20
max_num_chars = 40
num_lines = 10

# Gen texts
num_chars = 20



def gen_lines(ttfs):
    
    for ttf in ttfs:
    	image_savepath = "../databases/lines/" + ttf.split(".")[0].lower() + "/images/"
    	groundtruth_savepath = "../databases/lines/" + ttf.split(".")[0].lower() + "/groundtruth/"
        
    	if not os.path.exists(image_savepath):
    		os.makedirs(image_savepath)
    	if not os.path.exists(groundtruth_savepath):
    		os.makedirs(groundtruth_savepath)
            
    	if ttf.split(".")[0].lower() == "copiale":
            selected_alphabet = alphabet_copiale
            border = (200, 10, 200, 10)
    	else:
            selected_alphabet = alphabet_default
            border = (20, 10, 20, 10)
            
            
    	font = ImageFont.truetype("../ciphers/" + ttf, size=120)
        
    	props = [5]*len(selected_alphabet)
    	props[-1] = 15
        
    	pack = []
    
    	while len(pack) <= num_lines:
            pack.append(''.join(random.choices(selected_alphabet,weights=props)[0] for i in range(random.randint(min_num_chars,max_num_chars)))+"\n")
    
    	im = Image.new('L',(1,1),color=255)
    	scratch_draw = ImageDraw.Draw(im)
    	for index,text in enumerate(pack):
            textsize = scratch_draw.multiline_textsize(text,font=font,spacing=-10)
    		
            im = Image.new('L',textsize,)
            draw = ImageDraw.Draw(im)
            draw.multiline_text(xy=(0,0),text=text,fill=255,font=font,spacing=-10)
            im = ImageOps.invert(im)
            im = ImageOps.expand(im, border=border, fill="white")
            im.save(image_savepath+ttf.split(".")[0].lower()+"_"+str(index)+".png","PNG")
            
            f = open(groundtruth_savepath+ttf.split(".")[0].lower()+"_"+str(index)+".txt","w")
            f.write(text)
                


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
               border = (200, 10, 200, 10)
    	else:
               selected_alphabet = alphabet_default
               border = (20, 10, 20, 10)
            
    	font = ImageFont.truetype("../ciphers/" + ttf, size=120)
    	file_char = random.choice(files)
    	file = open("../texts/" + file_char,"r",encoding = "UTF-8")
        
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

    	im = Image.new('L',(1,1),color=255)
    	scratch_draw = ImageDraw.Draw(im)
    	for index,text in enumerate(pack):
    		textsize = scratch_draw.multiline_textsize(text,font=font,spacing=40)
    		
    		im = Image.new('L',textsize,)
    		draw = ImageDraw.Draw(im)
    		draw.multiline_text(xy=(0,0),text=text,fill=255,font=font,spacing=40)
    		im = ImageOps.invert(im)
    		im.save(image_savepath+ttf.split(".")[0].lower()+"_"+str(index)+".png","PNG")

    		f = open(groundtruth_savepath+ttf.split(".")[0].lower()+"_"+str(index)+".txt","w")
    		f.write(text)



if __name__ == '__main__':
	#gen_lines(ttfs)
    #gen_txt(ttfs, files)
    
    pass
    
    