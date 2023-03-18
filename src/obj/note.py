from utils.define import PyGame


class Note:
    
    def __init__(self, speed = 1, time = 1) -> None:
        self.valid = True
        self.speed = speed
        self.time = time