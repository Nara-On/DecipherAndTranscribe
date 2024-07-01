from lark import Lark
from lark.exceptions import *

from pathlib import Path

from mido import MidiFile
from mido import MidiTrack
from mido import Message
from mido import MetaMessage

import json

import numpy as np

PARTIIION = "test"

LOG_FILE = Path(
    "/home/pau/Documents/midi_score/checkpoints/test5/test5_{}_92_output.log".format(
        PARTIIION
    )
)
MIDI_OUT = Path("/home/pau/Documents/midi_score/seq2seqICFHR/midi")
GROUNDTRUTH = Path("/home/pau/Documents/midi_score/datasets/syn_midi/syn_midi.json")


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


def parse_number(node):
    numbers = node.children[0].children
    numbers = [int(x.value.split("_")[1]) for x in numbers]
    value = sum([x * 10 ** (len(numbers) - i - 1) for i, x in enumerate(numbers)])

    return value


def process_tree(parse_tree):
    pending_notes = []
    full_notes = []
    time = 0

    track = MidiTrack()

    MetaMessage("text", text="creator: ", time=0),
    MetaMessage("text", text="Seq2Seq MIDI OMR", time=0),
    # track.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=18,
    #                          notated_32nd_notes_per_beat=8, time=0))
    track.append(MetaMessage("set_tempo", tempo=1000000, time=0))

    for event in parse_tree.children:

        event_type = None
        delta_time, pitch, velocity, channel = 0, 0, 90, 0

        for component in event.children:
            comp_type = component.data

            if comp_type == "delta":
                delta_time = parse_number(component)
                time += delta_time

            elif comp_type == "midi_noteon" or comp_type == "midi_noteoff":
                for param in component.children:
                    attribute = param.data
                    value = parse_number(param)

                    if attribute == "pitch":
                        pitch = value
                    elif attribute == "channel":
                        channel = value
                    elif attribute == "velocity":
                        velocity = value

                if comp_type == "midi_noteon":
                    event_type = "note_on"

                    pending_notes.append(
                        {
                            "pitch": pitch,
                            "channel": channel,
                            "velocity": velocity,
                            "start_time": time,
                            "end_time": 0,
                        }
                    )
                elif comp_type == "midi_noteoff":
                    event_type = "note_off"

                    for i in pending_notes:
                        if (
                            i["pitch"] == pitch
                            and i["channel"] == channel
                            and i["velocity"] == velocity
                        ):
                            pending_notes.remove(i)
                            i["end_time"] = time
                            full_notes.append(i)
                            break

        track.append(
            Message(event_type, note=pitch, velocity=velocity, time=delta_time)
        )
    track.append(MetaMessage("end_of_track", time=0))

    return track, full_notes, pending_notes


def create_parse_tree(log_data, filename, parser):
    try:
        parse_tree = parser.parse(log_data)
    except UnexpectedCharacters as exc:
        print("Filename {} has a malformed midi output: {}".format(filename, log_data))
        print("Parser message: {}".format(str(exc)))
        return None

    except UnexpectedToken as exc:
        print(
            "Filename {} contains unknown tokens or is malformed: {}".format(
                filename, log_data
            )
        )
        print("Parser message: {}".format(str(exc)))
        return None
    return parse_tree


def main():
    with open(GROUNDTRUTH, "r") as f_gt:
        groundtruth = json.loads(f_gt.read())
        groundtruth = groundtruth[PARTIIION]

    gt_transcripts = {}

    for x in groundtruth:
        gt_transcripts[x["midi_name"]] = " ".join(x["groundtruth"])

    with open("./midi_grammar.lark", "r") as f_grm:
        midi_grammar = f_grm.read()

    midi_parser = Lark(
        midi_grammar, parser="lalr", propagate_positions=False, maybe_placeholders=False
    )
    global_ser = 0
    low_perf_img = []
    pending_img = []

    with open(LOG_FILE, "r") as f_log:
        file_lines = 0  # Lines in the file
        good_lines = 0  # Correctly acquired lines

        for line in f_log:
            file_lines += 1
            filename, log_data = line.split("|")

            midi_filename = filename.split(".")[0] + ".midi"

            # Parse the predicted output
            parse_tree = create_parse_tree(log_data, filename, midi_parser)

            if parse_tree is None:
                # Consistency check (in case the tree is not legal)
                continue

            good_lines += 1

            # Create Midi file
            mid = MidiFile(ticks_per_beat=384)

            pred_track, pred_full, pred_pending = process_tree(parse_tree)

            if len(pred_pending) > 0:
                pending_img.append(filename)

            mid.tracks.append(pred_track)
            mid.save(MIDI_OUT / midi_filename)

            # Open groundtruth transcript and parse it
            gt_tree = create_parse_tree(
                gt_transcripts[midi_filename], filename, midi_parser
            )
            (
                _,
                gt_full,
                _,
            ) = process_tree(gt_tree)

            # Study differences between the GT and the Prediction
            if len(pred_full) > 0 and len(gt_full) > 0:
                file_ser, _ = levenshtein(pred_full, gt_full)
            elif (len(pred_full) > 0 and len(gt_full) == 0) or (
                len(pred_full) == 0 and len(gt_full) > 0
            ):
                file_ser = 1.0
            else:
                file_ser = 0.0
            global_ser += file_ser

            if file_ser > 0.1:
                low_perf_img.append(filename)

        print(
            "Total lines: {}\n"
            "Correctly parsed lines: {:.04} %\n"
            "Note error rate on correct lines: {:.04} %".format(
                file_lines,
                (good_lines / file_lines) * 100,
                (global_ser / good_lines) * 100,
            )
        )
        print("\n\nLow Performance Files (> 10% SER) ({}): ".format(len(low_perf_img)))
        for f in low_perf_img:
            print("\t", f)

        print(
            "\n\nImages with unclosed notes (No NOTE_OFF for a given a NOTE_ON) ({})".format(
                len(pending_img)
            )
        )
        for f in pending_img:
            print("\t", f)


if __name__ == "__main__":
    main()
