from mido import MidiFile
from mido import MidiTrack
from mido import Message
from mido import MetaMessage
from midi2audio import FluidSynth

text_file = open("pred_logs/test_predict_seq.59.log", "r")
lines = text_file.readlines()
count = 0
auxcount = 0
newlines = []
filename = []

for line in lines:
    filename.append(line[: line.rfind("|")])
    line = line.replace("\n", "")
    line = line[line.rfind("|") :]
    line = line.replace("|", "")
    newlines.append(line)

for aux in newlines:
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=1000000))
    aux = aux.split("~")
    for word in aux:
        auxword = word.split(".")
        for letter in auxword:
            if count == 0:
                vnote = (letter[letter.rfind("=") :]).replace("=", "")
            if count == 1:
                vvelocity = (letter[letter.rfind("=") :]).replace("=", "")
            if count == 2:
                vtime = (letter[letter.rfind("=") :]).replace("=", "")
            count = count + 1
        count = 0
        track.append(
            Message(
                "note_on", note=int(vnote), velocity=int(vvelocity), time=int(vtime)
            )
        )
    mid.save("midi/" + str(filename[auxcount]) + "_syn_beethoven.mid")
    fs = FluidSynth()
    fs.midi_to_audio(
        "midi/" + str(filename[auxcount]) + "_syn_beethoven.mid",
        "wav/" + str(filename[auxcount]) + "_syn_beethoven.wav",
    )
    print(str(filename[auxcount]) + "_syn_beethoven.mid")
    auxcount = auxcount + 1
