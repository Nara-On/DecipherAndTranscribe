from main_torch_latest import all_data_loader, test
import argparse

# import os
import pdb
import numpy as np
import time


def levenshtein(source, target):
    matrix = []
    # if len(source) < len(target):
    # return levenshtein(target, source)
    # So now we have len(source) >= len(target).
    if len(target) == 0:
        return len(source)

    # We call tuple() to force strings to be used as sequences
    # ('c', 'a', 't', 's') - numpy uses them as values by default.
    source = np.array(tuple(source))
    target = np.array(tuple(target))

    # We use a dynamic programming algorithm, but with the
    # added optimization that we only need the last two rows
    # of the matrix.
    previous_row = np.arange(target.size + 1)
    # print previous_row

    matrix.append(previous_row)
    for s in source:
        # Insertion (target grows longer than source):
        current_row = previous_row + 1

        # Substitution or matching:
        # Target and source items are aligned, and either
        # are different (cost of 1), or are the same (cost of 0).

        current_row[1:] = np.minimum(
            current_row[1:], np.add(previous_row[:-1], target != s)
        )

        # Deletion (target grows shorter than source):
        current_row[1:] = np.minimum(current_row[1:], current_row[0:-1] + 1)

        previous_row = current_row
        matrix.append(previous_row)
        # print previous_row
    return [previous_row[-1] / float(len(target)), matrix]


parser = argparse.ArgumentParser(description="test")
parser.add_argument("epoch", type=int, help="epoch that you want to evaluate")
args = parser.parse_args()

_, _, test_loader = all_data_loader()
test(test_loader, args.epoch, showAttn=True)
gt = "/home/daniel/Escritorio/midiseq/seq2seqICFHR/RWTH.iam_word_gt_final.test.thresh"

decoded = "pred_logs/test_predict_seq." + str(args.epoch) + ".log"

filegt = open(gt, "r")
fileprediction = open(decoded, "r")

gtlines = []
for line in filegt:
    gtlines.append(line)

predictionlines = []
for line in fileprediction:
    predictionlines.append(line)

filegt.close()
fileprediction.close()
resultAcum = 0
contad = 0

listError = []

for indPred in range(0, len(predictionlines)):
    currentSplit = predictionlines[indPred].split("\n")[0].split("|")
    for indgt in range(0, len(gtlines)):
        if currentSplit[0] == gtlines[indgt].split("|")[0]:
            resultLeven = levenshtein(
                currentSplit[1].split("~"),
                gtlines[indgt].split("\n")[0].split("|")[1].split("~"),
            )
            listError.append([currentSplit[0], resultLeven[0]])
            resultAcum += resultLeven[0]
            contad += 1

print("CER: " + str(((resultAcum / contad) * 100)) + "%")

result = sorted(listError, key=lambda x: (x[1], x[0]))
print(result)


print(time.ctime())
