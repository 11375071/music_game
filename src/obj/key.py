from utils.define import PyGame
from typing import List
from obj.note import Note

def press(notes: List[Note]):
    for note in notes:
        if note.valid == False:
            continue
        if abs(note.time) < 0.06:
            print("perfect")
            return
        if abs(note.time) < 0.1:
            print("good")
            return
        if note.time < 0.15:
            note.valid = False
            print("miss")
            return
        