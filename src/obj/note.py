from utils.define import PyGame
import utils.color as color


class Note:

    def __init__(
        self,
        game: PyGame, align: str = "center",
        speed: float = 4, time: float = 1, size: tuple = (50, 10),
        color: tuple = color.AliceBlue, destination: tuple = (100, 100)
    ) -> None:
        self.game = game
        self.align = align
        self.speed = speed
        self.time = time
        self.size = size
        self.color = color
        self.destination = destination

        self.rank_type = "none"
        self.appear = True

        self.align_destination()

    def align_destination(self):
        if self.align == "center":
            self.destination = self.destination[0] - self.size[0] / 2, \
                self.destination[1] - self.size[1] / 2
        elif self.align == "right-up":
            self.destination = self.destination[0] - self.size[0], \
                self.destination[1]
        elif self.align == "right-down":
            self.destination = self.destination[0] - self.size[0], \
                self.destination[1] - self.size[1]
        elif self.align == "left-down":
            self.destination = self.destination[0], self.destination[1] - self.size[1]
        # else: left-up

    def rank(self, rank_type: str):
        self.rank_type = rank_type

    def resolved(self):
        self.appear = False

    def render(self):
        if not self.appear:
            return
        self.pos = (
            self.destination[0],
            self.destination[1] - 50 * self.time * self.speed
        )
        self.background = self.game.it.Surface(self.size)
        self.background.fill(self.color)
        self.game.screen.blit(self.background, self.pos)
