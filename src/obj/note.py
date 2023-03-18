from utils.define import PyGame

class Note:
    
    def __init__(
        self,
        game: PyGame,
        speed: float = 1, time: float = 1, size: tuple = (50, 10),
        color: tuple = None, destination: tuple = (100, 100)
    ) -> None:
        self.game = game
        self.valid = True
        self.speed = speed
        self.time = time
        self.size = size
        self.color = color
        self.destination = destination

    def render(self):
        self.pos = (self.destination[0], self.destination[1] - 50 * self.time * self.speed)
        self.background = self.game.it.Surface(self.size)
        self.background.fill(self.color)
        self.game.screen.blit(self.background, self.pos)