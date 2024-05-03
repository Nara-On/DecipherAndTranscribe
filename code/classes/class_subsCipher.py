# -*- coding: utf-8 -*-

class Ciphers:
    
    def __init__(self, alph):
        """
        Initialization of class values
        
        Inputs: 
            - alph = List of alphabets (List of strings)
        
        """ 
        self.alphabet = alph
    
    
    def ceaser_encoder(self, message, key):
        """
        Ceaser encoder
        
        Inputs: 
            - message = Message to be encoded (str)
            - alph = List of alphabets (List of strings)
        
        """ 
        ciphertext = ""
        for c in message:
            if c == " " or c == "\n":
                ciphertext += c
            else:
                ciphertext += self.alphabet[(self.alphabet.index(c) + key) % len(self.alphabet)]
        return ciphertext


    def ceaser_decoder(self, ciphertext, key):
        """
        Ceaser decoder
        
        Inputs: 
            - ciphertext = Encoded text (str)
            - key = Number of shifts (int)
        
        """ 
        message = ""
        for c in ciphertext:
            if c == " " or c == "\n":
                message += c
            else:
                message += self.alphabet[(self.alphabet.index(c) - key) % len(self.alphabet)]
        return message
    
    