# -*- coding: utf-8 -*-

import seaborn as sns
import matplotlib.pyplot as plt

import numpy as np
import json 

from seq_recog.utils.io import load_pickle_prediction
from pathlib import Path

from argparse import ArgumentParser, Namespace

import pkl2json as pkl


root = "../../databases/data/tr_02/results/"

if __name__ == "__main__":
    
    train200 = ["stl25le1", "2giyfbxj", "ua4bgxid", "0cmoqj5k", "gaoyaidz",
             "q1c2g7tm", "3r1a0ff5"]
    
    # 200 epochs
    for training in train200:        
        output_e200 = load_pickle_prediction(Path(root + "dummy-" + training + "/e200_train/metric_levenshtein.pkl"))
        output_best = load_pickle_prediction(Path(root + "dummy-" + training + "/best_eval/metric_levenshtein.pkl"))
        outputs_txt = load_pickle_prediction(Path(root + "dummy-" + training + "/best_eval/results_text.pkl"))
        
        predictions_e200 = {k: pkl.unarray(v) for k, v in output_e200.items()}
        predictions_best = {k: pkl.unarray(v) for k, v in output_best.items()}
        predictions_txt = {k: pkl.unarray(v) for k, v in outputs_txt.items()}
        """
        with open("../../visuals/results/pkl/" + training + "_e200_train.json", "w") as f_out:
            json.dump(predictions_e200, f_out, indent=4)
        with open("../../visuals/results/pkl/" + training + "_best_eval.json", "w") as f_out:
            json.dump(predictions_best, f_out, indent=4)
        with open("../../visuals/results/pkl/" + training + "_text_results.json", "w") as f_out:
            json.dump(predictions_txt, f_out, indent=4)   
        """
    
    # 500 epochs
    output_e500 = load_pickle_prediction(Path(root + "dummy-ph7ybv4l/e500_train/metric_levenshtein.pkl"))
    output_best = load_pickle_prediction(Path(root + "dummy-ph7ybv4l/best_eval/metric_levenshtein.pkl"))
    outputs_txt = load_pickle_prediction(Path(root + "dummy-ph7ybv4l/best_eval/results_text.pkl"))
    
    predictions_e500 = {k: pkl.unarray(v) for k, v in output_e500.items()}
    predictions_best = {k: pkl.unarray(v) for k, v in output_best.items()}
    predictions_txt = {k: pkl.unarray(v) for k, v in outputs_txt.items()}
    """
    with open("../../visuals/results/pkl/" + training + "_e200_train.json", "w") as f_out:
        json.dump(predictions_e500, f_out, indent=4)
    with open("../../visuals/results/pkl/" + training + "_best_eval.json", "w") as f_out:
        json.dump(predictions_best, f_out, indent=4)
    with open("../../visuals/results/pkl/" + training + "_text_results.json", "w") as f_out:
        json.dump(predictions_txt, f_out, indent=4)      
    """
    
    # Convergence ¿?
    uniqueNums = []
    maxInds = []
    
    for lindar in [32, 64, 96, 127]:
        countMany = 0
        
        maxInd = 0
        for image, text in zip(predictions_txt, predictions_txt.values()):
            unique, counts = np.unique(text, return_counts=True)
            if np.max(unique) > maxInd:
                maxInd = np.max(unique)
            
            for u, c in zip(unique, counts):
                if c >= lindar:
                    if u not in [0,1,2,3]: 
                        countMany += 1
                        break
        uniqueNums.append(countMany)
        maxInds.append(maxInd)
        
    q1 = uniqueNums[0]/len(predictions_txt)*100    # more than 32   = 48 %     # 23 %
    q2 = uniqueNums[1]/len(predictions_txt)*100    # more than 64   = 19 %     #  7 %
    q3 = uniqueNums[2]/len(predictions_txt)*100    # more than 96   =  5 %     #  5 %
    q4 = uniqueNums[3]/len(predictions_txt)*100    # 127            =  0 %     #  0 %








