from utils.define import PyGame

def press(self, notes):
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
        