# -*- coding: utf-8 -*-

import classes.class_loadDataset as lD


if __name__ == '__main__':
    
    """
    # Load Dataset: First Transcription (test)
    dataset = lD.LoadDataset("../databases/data/tr_01/", 1502,
                                 "../databases/copiale_real-vs-sint/sint/images/", 
                                 "../databases/copiale_real-vs-sint/sint/transcriptions/")
    dataset.load_dataset_tr(0.8, 0.1)
       
    
    # Load Dataset: Transcription with Augmentation
    dataset = lD.LoadDataset("../databases/data/tr_02/", 1502, 
                                 "../databases/copiale_real-vs-sint/sint/images/", 
                                 "../databases/copiale_real-vs-sint/sint/transcriptions/",
                                 "../databases/copiale_real-vs-sint/sint/augmentation/")
    dataset.load_dataset_tr(0.8, 0.1)
    
    
    # Load Dataset: Augmentations Only
    dataset = lD.LoadDataset("../databases/data/tr_03/", 4507,
                                 "../databases/copiale_real-vs-sint/sint/augmentation/", 
                                 "../databases/copiale_real-vs-sint/sint/groundtruth_augmentation/")
    dataset.load_dataset_tr(0.8, 0.1)
    
    """
    # Load Dataset: Decipherment task
    dataset = lD.LoadDataset("../databases/data/de_01/", 1502, 
                                 "../databases/copiale_real-vs-sint/sint/images/", 
                                 "../databases/copiale_real-vs-sint/real/deciphered/",
                                 "../databases/copiale_real-vs-sint/sint/augmentation/")
    dataset.redo_files_de(0.8, 0.1)