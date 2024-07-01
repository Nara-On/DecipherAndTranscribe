import os

list = []
folderDelete = "save_weights/"
for r, d, files in os.walk(folderDelete):
    for f in files:
        list.append(int(f.split(".model")[0].split("seq2seq-")[1]))
list.sort(reverse=True)

for i in range(25, len(list)):
    os.remove(folderDelete + "seq2seq-" + str(list[i]) + ".model")
