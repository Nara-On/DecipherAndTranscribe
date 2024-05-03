# -*- coding: utf-8 -*-

import os
import warnings

import classes.class_copiale as cop
import classes.class_cipherGenerator as gen
import classes.class_augmentation as aug

warnings.filterwarnings("ignore", category = DeprecationWarning) 


# Files
ttfs = ["Masonic_Cipher.ttf","KeilFont.ttf","Stickman.ttf", 
        "Copiale.ttf","ModernRunic-Regular.ttf", "PigpenCipher.otf"]

lines = ["quotes.txt"]
texts = ["mid_ElEscorpionYLaRana.txt", "mid_RimaLIII.txt", 
         "mid_TheGrasshopper.txt", "mid_TheHareAndTheTortoise.txt"]

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


###########################################################################################################

if __name__ == '__main__':
    
    copiale = cop.Copiale(1502)
    generator = gen.CipherGenerator(ttfs, alphabets, texts, lines)
    augmentation = aug.Augmentation(3)
    
    #generator.gen_randlines("../databases/lines/", 200)
    generator.gen_lines("../databases/lines/")
    
    generator.gen_texts("../databases/texts/")
    
    for ttf, alph in zip(ttfs, alphabets):
        generator.test_lines(ttf, alph, "../databases/trials/lines/")
        generator.test_texts(ttf, "mid_Ozymandias.txt", alph, "../databases/trials/texts/")
    
    copiale.print_alphabet()
    copiale.gen_realLines("../databases/copiale_real-vs-sint/sint/")
    
    augmentation.augmentator(os.listdir("../databases/copiale_real-vs-sint/sint/images"), 
                             '../databases/copiale_real-vs-sint/sint/images/',
                             "../databases/copiale_real-vs-sint/sint/augmentation/")
    