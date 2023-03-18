from utils.define import PyGame


class Key:

    def press(self, notes):
        for note in notes:
            if note.valid == False:
                continue
            if abs(note.time) < 0.06:
                return "perfect"
            if abs(note.time) < 0.1:
                return "good"
            if note.time < 0.15:
                note.valid = False
                return "miss"
        