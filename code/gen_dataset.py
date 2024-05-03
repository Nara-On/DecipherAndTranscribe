# -*- coding: utf-8 -*-

import classes.class_loadDataset as lD

size = 1502


###########################################################################################################

if __name__ == '__main__':
    
    """
    # Load Dataset (Test)
    dataset = lD.LoadDataset("../databases/data/tr-00/", size, "../databases/copiale_real-vs-sint/sint/images/", 
                                             "../databases/copiale_real-vs-sint/sint/transcriptions/")
    dataset.loadDataset(0.8, 0.1)
    """
    
    # Load Dataset First Transcription
    dataset = lD.LoadDataset("../databases/data/tr-01/", size, "../databases/copiale_real-vs-sint/sint/images/", 
                                             "../databases/copiale_real-vs-sint/sint/transcriptions/")
    dataset.loadDataset(0.8, 0.1)