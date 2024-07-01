# -*- coding: utf-8 -*-

import classes.class_loadDataset as lD


if __name__ == '__main__':
    
    """
    # Load Dataset: First Transcription (tr_01)
    dataset = lD.LoadDataset("../databases/data/tr_01/", 1502,
                                 "../databases/copiale_real-vs-sint/sint/images/", 
                                 "../databases/copiale_real-vs-sint/sint/transcriptions/")
    #dataset.load_dataset(0.8, 0.1, "tr")
    dataset.load_json_only(0.8, 0.1, "tr")
    

    # Load Dataset: Transcription with Augmentation SINT code v1 (tr_02)
    dataset = lD.LoadDataset("../databases/data/tr_02/", 1502, 
                                 "../databases/copiale_real-vs-sint/sint/images/", 
                                 "../databases/copiale_real-vs-sint/sint/transcriptions/",
                                 "../databases/copiale_real-vs-sint/sint/augmentations/")
    dataset.load_dataset(0.8, 0.1, "tr")
    dataset.load_json_only(0.8, 0.1, "tr")

    
    # Load Dataset: Transcription with Augmentation SINT code v2 (tr_03)
    dataset = lD.LoadDataset("../databases/data/tr_03/", 1502, 
                                 "../databases/copiale_real-vs-sint/sint/images/", 
                                 "../databases/copiale_real-vs-sint/sint/transcriptions/",
                                 "../databases/copiale_real-vs-sint/sint/augmentations/")
    dataset.load_dataset(0.8, 0.1, "tr")
    dataset.load_json_only(0.8, 0.1, "tr") 

    
    # Load Dataset: Transcription with Augmentation REAL (tr_04)
    dataset = lD.LoadDataset("../databases/data/tr_04/", 1502, 
                                 "../databases/copiale_real-vs-sint/real/images/", 
                                 "../databases/copiale_real-vs-sint/real/groundtruth/",
                                 "../databases/copiale_real-vs-sint/real/augmentations/")
    #dataset.load_dataset(0.8, 0.1, "tr")
    dataset.load_json_only(0.8, 0.1, "tr")
    

    # Load Dataset: Transcription with Augmentation MIX (tr_05)
    dataset = lD.LoadDatasetCustom("../databases/data/tr_05/", 
                                   "../databases/copiale_real-vs-sint/sint/images/", 
                                   "../databases/copiale_real-vs-sint/sint/transcriptions/", 1502,
                                   
                                   "../databases/copiale_real-vs-sint/real/images/", 
                                   "../databases/copiale_real-vs-sint/real/groundtruth/", 1502,
                                   
                                   "../databases/copiale_real-vs-sint/sint/augmentations/")
    
    #dataset.load_dataset(1, 1, "tr")
    dataset.load_json_only(1, 1, "tr")
    
     """     
    # Load Dataset: Decipherment with Augmentation SINT (de_01)
    dataset = lD.LoadDataset("../databases/data/de_01/", 1502, 
                                 "../databases/copiale_real-vs-sint/sint/images/", 
                                 "../databases/copiale_real-vs-sint/real/deciphered/",
                                 "../databases/copiale_real-vs-sint/sint/augmentations/")
    #dataset.load_dataset(0.8, 0.1, "de")
    dataset.load_json_only(0.8, 0.1, "de")
 
    
    # Load Dataset: Decipherment with Augmentation REAL (de_02)
    dataset = lD.LoadDataset("../databases/data/de_02/", 1502, 
                                 "../databases/copiale_real-vs-sint/real/images/", 
                                 "../databases/copiale_real-vs-sint/real/deciphered/",
                                 "../databases/copiale_real-vs-sint/real/augmentations/")
    
    #dataset.load_dataset(0.8, 0.1, "de")
    dataset.load_json_only(0.8, 0.1, "de")
    
   
    # Load Dataset: Decipherment with Augmentation MIX (de_03)
    dataset = lD.LoadDatasetCustom("../databases/data/de_03/", 
                                   "../databases/copiale_real-vs-sint/sint/images/", 
                                   "../databases/copiale_real-vs-sint/real/deciphered/", 1502,
                                   
                                   "../databases/copiale_real-vs-sint/real/images/", 
                                   "../databases/copiale_real-vs-sint/real/deciphered/", 1502,
                                   
                                   "../databases/copiale_real-vs-sint/sint/augmentations/")
    
    #dataset.load_dataset(1, 1, "de")
    dataset.load_json_only(1, 1, "de")
   
    
    
    
    