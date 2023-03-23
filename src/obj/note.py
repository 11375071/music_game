from utils.define import PyGame
import utils.color as color


class Note:

    def __init__(
        self,
        game: PyGame, align: str = "center",
        speed: float = 11, init_time: float = 1, time: float = 1, size: tuple = (50, 10),
        color: tuple = color.AliceBlue, destination: tuple = (100, 100)
    ) -> None:
        self.game = game
        self.align = align
        self.speed = speed
        self.init_time = init_time
        self.time = time
        self.size = size
        self.color = color
        self.destination = destination

        self.rank_type = "none"
        self.appear = True

        self.align_destination()

    def align_destination(self):
        if self.align == "center":
            self.destination_align = self.destination[0] - self.size[0] / 2, \
                self.destination[1] - self.size[1] / 2
        elif self.align == "right-up":
            self.destination_align = self.destination[0] - self.size[0], \
                self.destination[1]
        elif self.align == "right-down":
            self.destination_align = self.destination[0] - self.size[0], \
                self.destination[1] - self.size[1]
        elif self.align == "left-down":
            self.destination_align = self.destination[0], self.destination[1] - self.size[1]
        else: 
            self.destination_align = self.destination[0], self.destination[1]

    def rank(self, rank_type: str):
        self.rank_type = rank_type

    def resolved(self):
        self.appear = False

    def render(self):
        if not self.appear:
            return
        self.pos = (
            self.destination_align[0],
            self.destination_align[1] - 50 * self.time * self.speed
        )
        self.background = self.game.it.Surface(self.size)
        self.background.fill(self.color)
        self.game.screen.blit(self.background, self.pos)
