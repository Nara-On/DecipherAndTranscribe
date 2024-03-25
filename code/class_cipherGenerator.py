# -*- coding: utf-8 -*-

from PIL import ImageFont, ImageDraw, Image, ImageOps
import random
import os


class CipherGenerator:
    
    def __init__(self, ttfs, alph, texts, lines):
        
        self.ttfs = ttfs
        self.alphabets = alph
        self.texts = texts
        self.lines = lines
        
        # Default values
        self.min_chars = 20
        self.max_chars = 40
        self.num_chars = 25
    
    
    def createImage(self, txt, ttf, image_savepath, groundtruth_savepath):
        """
        Generator of randomized lines
        
        """
        
        # Read cipher file
        font = ImageFont.truetype("../ciphers/" + ttf, size=120)
        
        # Create background image
        im = Image.new('L',(1,1), color=255)
        scratch_draw = ImageDraw.Draw(im)
        
        # Calculate size text
        textsize = scratch_draw.multiline_textsize(txt, font=font, spacing=-10)
        
        if "Copiale" in ttf:
            padding = (50, 50)  # Adjust padding as needed
            textsize = (textsize[0] + padding[0], textsize[1] + padding[1])
            start_position = ((padding[0]) // 2, 0)
        else:
            start_position = (0, 0)
        
        # Create final image
        im = Image.new('L', textsize,)
        draw = ImageDraw.Draw(im)
        draw.multiline_text(xy=start_position, text=txt, fill=255, font=font, spacing=-10)
        
        # Border
        im = ImageOps.invert(im)
        im = ImageOps.expand(im, border=(20, 10, 20, 10), fill="white")
        im.save(image_savepath,"PNG")
            
        f = open(groundtruth_savepath,"w")
        f.write(txt)
        f.close()   
        
        
    def gen_randlines(self, savepath, num_lines):
        """
        Generator of randomized lines
        
        """
        
        for ttf, alph in zip(self.ttfs, self.alphabets):
            print("Generating random lines from " + ttf.split(".")[0].lower() + "...")
            
            # Create savepath routes
            image_savepath = savepath + ttf.split(".")[0].lower() + "/images/"
            groundtruth_savepath = savepath + ttf.split(".")[0].lower() + "/groundtruth/"
            
            # Generate directories if necessary
            if not os.path.exists(image_savepath):
                os.makedirs(image_savepath)
            if not os.path.exists(groundtruth_savepath):
                os.makedirs(groundtruth_savepath)
            
            # Parameters for the generation of randomized lines
            props = [5]*len(alph)
            props[-1] = 15
            pack = []
            
            # Generate randomized lines
            while len(pack) <= num_lines:
                pack.append(''.join(random.choices(alph, weights=props)[0] for i in range(random.randint(self.min_chars, self.max_chars)))+"\n")
            
            # Copy text into the background image
            for index,text in enumerate(pack):
                self.createImage(text, ttf, image_savepath + ttf.split(".")[0].lower() + "_" + str(index) + ".png", 
                                 groundtruth_savepath + ttf.split(".")[0].lower() + "_"+str(index) + ".txt")

    
    
    def gen_lines(self, savepath):
        """
        Generator of lines from txt files
        
        """
        
        for ttf in self.ttfs:
            print("Generating lines from " + ttf.split(".")[0].lower() + "...")
            
            # Create savepath routes
            image_savepath = savepath + ttf.split(".")[0].lower() + "/images/"
            groundtruth_savepath = savepath + ttf.split(".")[0].lower() + "/groundtruth/"
            
            # Generate directories if necessary
            if not os.path.exists(image_savepath):
                os.makedirs(image_savepath)
            if not os.path.exists(groundtruth_savepath):
                os.makedirs(groundtruth_savepath)
            
            # Parameters for the generation of randomized lines
            index = 0
            
            for file_char in self.lines:
                print("- File " + file_char.split(".")[0].lower())
                
                # Read text file
                l = open("../texts/" + file_char, "r")
                
                for txt in l.readlines():
                    self.createImage(txt.strip(), ttf, image_savepath + ttf.split(".")[0].lower() + "_" + str(index) + ".png", 
                                     groundtruth_savepath + ttf.split(".")[0].lower() + "_" + str(index) + ".txt")
                    index += 1
                l.close()
    
    
    def gen_texts(self, savepath):
        """
        Generator of text images from txt files
        
        """
        for ttf, alph in zip(self.ttfs, self.alphabets):
            print("Generating text from " + ttf.split(".")[0].lower() + "...")
            
            # Create savepath routes
            image_savepath = savepath + ttf.split(".")[0].lower() + "/images/"
            groundtruth_savepath = savepath + ttf.split(".")[0].lower() + "/groundtruth/"
            
            # Generate directories if necessary
            if not os.path.exists(image_savepath):
                os.makedirs(image_savepath)
            if not os.path.exists(groundtruth_savepath):
                os.makedirs(groundtruth_savepath)
            
            # Image index
            index = 0
            
            for file_char in self.texts:
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
                        if c in alph:
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
                    if countChar < self.num_chars:
                        justified_text += " "
                    else:
                        countChar = 0
                        countLine += 1
                        if countLine < self.num_chars:
                            justified_text += " \n "
                        else:
                            countLine = 0
                            pack.append(justified_text)
                            justified_text = " "
                            
                for text in pack:
                    self.createImage(text, ttf, image_savepath + ttf.split(".")[0].lower() + "_" + str(index) + ".png", 
                                     groundtruth_savepath + ttf.split(".")[0].lower() + "_" + str(index) + ".txt")
                    index += 1
        
        
    def test_lines(self, ttf, text, savepath):
        """
        Generator of lines from a txt file
        
        Inputs: 
            - ttfs = Cipher files
            - text = Text file
        
        """
        
        # Generate directories if necessary
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        
        # Create image
        self.createImage(text, ttf, savepath+ ttf.split(".")[0].lower() + ".png", 
                         savepath + ttf.split(".")[0].lower() + ".txt")
            
        
    def test_texts(self, ttf, file, alphabet, savepath):
        """
        Generator of text images from a txt file
        
        """
        
        # Generate directories if necessary
        if not os.path.exists(savepath):
            os.makedirs(savepath)
            
        # Read text file
        file = open("../texts/" + file, "r", encoding="UTF-8")
        
        # Filter characters
        big_text = ""
        for line in file:
            line = line.rstrip()
            line = line.lower()
            filtered = ""
            for c in line:
                if c in alphabet:
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
            if countChar < self.num_chars:
                justified_text += " "
            else:
                countChar = 0
                countLine += 1
                if countLine < self.num_chars:
                    justified_text += " \n "
                else:
                    countLine = 0
                    pack.append(justified_text)
                    justified_text = " "
        
        # If text is too short, append it anyway
        if len(pack) == 0:
            pack.append(justified_text)
        
        # Copy text into the background image
        for text in pack:
            self.createImage(text, ttf, savepath+ ttf.split(".")[0].lower() + ".png", 
                             savepath + ttf.split(".")[0].lower() + ".txt")
