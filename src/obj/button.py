from pygame import event
from typing import Callable, Optional
from utils.define import PyGame
import utils.color as color


class Button:
    def __init__(
        self,
        game: PyGame,
        size: tuple, pos: tuple, align: str = "center",
        bg_color: tuple = color.PaleGreen2, bg_alpha: float = 1,
        image: Optional[str] = None,
        click_func: Optional[Callable] = None,
        key: Optional[int] = None,
        only_use_key: bool = False,
    ):
        self.game = game
        self.size = size
        self.pos = pos
        self.align = align
        self.bg_color = bg_color
        self.bg_alpha = bg_alpha
        self.click_func = click_func
        self.image = image
        self.key = key
        self.only_use_key = only_use_key
        self.change_background()
        self.align_position()

    def change_background(self):
        if self.image is not None:
            self.background = self.game.it.image.load(self.image)
            self.background = self.game.it.transform.scale(
                self.background, self.size
            )
        else:
            self.background = self.game.it.Surface(self.size)
            self.background.fill(self.bg_color)
            self.background.set_alpha(int(256 * self.bg_alpha))

    def align_position(self):
        if self.align == "center":
            self.pos_align = self.pos[0] - self.size[0] / 2, \
                self.pos[1] - self.size[1] / 2
        elif self.align == "right-up":
            self.pos_align = self.pos[0] - self.size[0], self.pos[1]
        elif self.align == "right-down":
            self.pos_align = self.pos[0] - self.size[0], self.pos[1] - self.size[1]
        elif self.align == "left-down":
            self.pos_align = self.pos[0], self.pos[1] - self.size[1]
        else:
            self.pos_align = self.pos

        # click rect
        self.rect = self.game.it.Rect(self.pos_align, self.size)

    def render(self):
        self.game.screen.blit(self.background, self.pos_align)

    def click_check(self, event: event.Event):
        if self.click_func is not None:
            pos = self.game.it.mouse.get_pos()
            if not self.only_use_key:
                if event.type == self.game.it.MOUSEBUTTONDOWN:
                    if self.game.it.mouse.get_pressed()[0]:
                        if self.rect.collidepoint(*pos):
                            self.click_func()
            if self.key is not None:
                if event.type == self.game.it.KEYDOWN:
                    if event.key == self.key:
                        self.click_func()


class TextButton(Button):
    def __init__(
        self,
        game: PyGame,
        text: str, pos: tuple, align: str = "center",
        font_family: str = "consolas", font_size: int = 100,
        color: tuple = color.PaleGreen2, bg_color: tuple = color.cyan,
        alpha: float = 1, bg_alpha: float = 1,
        click_func: Optional[Callable] = None,
        key: Optional[int] = None,
        only_use_key: bool = False,
    ):
        self.game = game
        self.pos = pos
        self.align = align
        self.bg_color = bg_color
        self.bg_alpha = bg_alpha
        self.click_func = click_func
        self.key = key
        self.only_use_key = only_use_key
        self.text = text
        self.font = self.game.it.font.SysFont(font_family, font_size)
        self.color = color
        self.alpha = alpha
        self.change_text(text)

    def change_text(self, text):
        self.text = text
        self.text = self.font.render(
            self.text, 1, [*self.color, self.alpha]
        )
        self.size = self.text.get_size()
        self.surface = self.game.it.Surface(self.size).convert_alpha()
        self.surface.fill([0, 0, 0, 0])
        self.surface.set_alpha(int(256 * self.alpha))
        self.surface.blit(self.text, (0, 0))
        self.background = self.game.it.Surface(self.size)
        self.background.fill(self.bg_color)
        self.background.set_alpha(int(256 * self.bg_alpha))
        self.align_position()

    def render(self):
        self.game.screen.blit(self.background, self.pos_align)
        self.game.screen.blit(self.surface, self.pos_align)
