from define import PyGame
import resource.color as color


class Button:

    def __init__(
        self,
        game: PyGame,
        text: str, pos: tuple, align: str = "center",
        font_family: str = "consolas", font_size: int = 100,
        color: tuple = color.PaleGreen2, bg_color: tuple = color.cyan,
        alpha: float = 1, bg_alpha: float = 1,
        click_func=None
    ):
        self.game = game
        self.text = text
        self.pos = pos
        self.align = align
        self.font = self.game.it.font.SysFont(font_family, font_size)
        self.color = color
        self.bg_color = bg_color
        self.alpha = alpha
        self.bg_alpha = bg_alpha
        self.click_func = click_func
        self.change_text()

    def change_text(self):
        self.text = self.font.render(
            self.text, 1, [*self.color , self.alpha]
        )
        self.size = self.text.get_size()
        self.surface = self.game.it.Surface(self.size).convert_alpha()
        self.surface.fill([0, 0, 0, 0])
        self.surface.set_alpha(int(256 * self.alpha))
        self.surface.blit(self.text, (0, 0))
        self.background = self.game.it.Surface(self.size)
        self.background.fill(self.bg_color)
        self.background.set_alpha(int(256 * self.bg_alpha))
        if self.align == "center":
            self.pos = self.pos[0] - self.size[0] / 2, \
                self.pos[1] - self.size[1] / 2
        elif self.align == "right-up":
            self.pos = self.pos[0] - self.size[0], self.pos[1]
        elif self.align == "right-down":
            self.pos = self.pos[0] - self.size[0], self.pos[1] - self.size[1]
        elif self.align == "left-down":
            self.pos = self.pos[0], self.pos[1] - self.size[1]
        # else: left-up

        # click rect
        self.rect = self.game.it.Rect(*self.pos, *self.size)

    def render(self):
        self.game.screen.blit(self.background, self.pos)
        self.game.screen.blit(self.surface, self.pos)

    def click_check(self, event):
        if self.click_func is not None:
            pos = self.game.it.mouse.get_pos()
            if event.type == self.game.it.MOUSEBUTTONDOWN:
                if self.game.it.mouse.get_pressed()[0]:
                    if self.rect.collidepoint(*pos):
                        self.click_func()
