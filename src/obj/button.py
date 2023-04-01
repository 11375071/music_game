from pygame import event
from typing import Callable, Optional
from utils.define import PyGame
import utils.color as color
import matplotlib.image as mpimg


class SimpleRect:
    def __init__(
        self, game: PyGame,
        size: tuple, pos: tuple, align: str = "center",
        color: tuple = color.PaleGreen2, alpha: float = 1,
        image: Optional[str] = None,
        strip_alpha: bool = False,
    ) -> None:
        """
        strip_alpha: if is true, click will dismiss area where alpha == 1
        """
        self.game = game
        self.size = size
        self.pos = pos
        self.align = align
        self.color = color
        self.alpha = alpha
        self.image = image
        self.strip_alpha = strip_alpha
        self.load_image = None
        self.change_image()
        self.align_position()

    def change_image(self):
        if self.image is not None:
            if self.strip_alpha:
                self.load_image = mpimg.imread(self.image)
            self.image = self.game.it.image.load(self.image)
            self.image = self.game.it.transform.scale(
                self.image, self.size
            )
        else:
            self.image = self.game.it.Surface(self.size)
            self.image.fill(self.color)
            self.image.set_alpha(int(256 * self.alpha))

    def align_position(self):
        if self.align == "center":
            self.pos_align = self.pos[0] - self.size[0] / 2, \
                self.pos[1] - self.size[1] / 2
        elif self.align == "right-up":
            self.pos_align = self.pos[0] - self.size[0], self.pos[1]
        elif self.align == "right-down":
            self.pos_align = self.pos[0] - \
                self.size[0], self.pos[1] - self.size[1]
        elif self.align == "left-down":
            self.pos_align = self.pos[0], self.pos[1] - self.size[1]
        else:  # "left-up"
            self.pos_align = self.pos

        # click rect
        self.rect = self.game.it.Rect(self.pos_align, self.size)

    def change_click_rect(self, pos: tuple, size):
        if self.align == "center":
            pos_align = pos[0] - size[0] / 2, \
                pos[1] - size[1] / 2
        elif self.align == "right-up":
            pos_align = pos[0] - size[0], pos[1]
        elif self.align == "right-down":
            pos_align = pos[0] - \
                size[0], pos[1] - size[1]
        elif self.align == "left-down":
            pos_align = pos[0], pos[1] - size[1]
        else:  # "left-up"
            pos_align = pos
        self.rect = self.game.it.Rect(pos_align, size)

    def collide(self, pos: tuple):
        if self.strip_alpha and self.load_image is not None:
            if not self.rect.collidepoint(*pos):
                return False
            return self.load_image[
                int(pos[1] / self.size[1] * self.load_image.shape[0])
            ][
                int(pos[0] / self.size[0] * self.load_image.shape[1])
            ][-1]
        else:
            return self.rect.collidepoint(*pos)

    def render(self):
        self.game.screen.blit(self.image, self.pos_align)


class SimpleButton(SimpleRect):
    def __init__(
        self, game: PyGame,
        size: tuple, pos: tuple, align: str = "center",
        color: tuple = color.PaleGreen2, alpha: float = 1,
        image: Optional[str] = None,
        strip_alpha: bool = False,
        click_func: Optional[Callable] = None,
        key: Optional[int] = None,
        only_use_key: bool = False,
        activate_on_keydown: bool = False,
        long_update: bool = False,
    ):
        """
        only_use_key: if False, you can both use key or mouse; or you can only use key
        activate_on_keydown: if False, it will activate on keyup; or it will activate on keydown
        long_update: activate many times if press for a long time
        """
        super().__init__(game, size, pos, align, color, alpha, image, strip_alpha)
        self.click_func = click_func
        self.key = key
        self.only_use_key = only_use_key
        self.activate_on_keydown = activate_on_keydown
        self.long_update = long_update
        self.long_press_frame = 0
        self.long_press_max = 25
        self.pressed = False
        self.__ready_to_click = False
        self.__ready_to_key = False

    def control_check(self):
        if self.click_func is not None:
            if self.activate_on_keydown and self.long_update:
                if self.pressed:
                    self.long_press_frame += 1
                else:
                    self.long_press_max = 25
                    self.long_press_frame = 0
                if self.long_press_frame >= self.long_press_max:
                    self.long_press_max = 10
                    self.long_press_frame = 0
                    self.click_func()

    def click_check(self, event: event.Event):
        if self.click_func is not None:

            if self.activate_on_keydown:
                if not self.only_use_key:
                    if event.type == self.game.it.MOUSEBUTTONDOWN:
                        pos = self.game.it.mouse.get_pos()
                        if self.collide(pos):
                            self.pressed = True
                            self.click_func()
                        else:
                            self.pressed = False
                    elif event.type == self.game.it.MOUSEBUTTONUP:
                        self.pressed = False
                if self.key is not None:
                    if event.type == self.game.it.KEYDOWN and event.key == self.key:
                        self.pressed = True
                        self.click_func()
                    if event.type == self.game.it.KEYUP and event.key == self.key:
                        self.pressed = False

            else:  # activate_on_keyup
                if not self.only_use_key:
                    if event.type == self.game.it.MOUSEBUTTONDOWN:
                        pos = self.game.it.mouse.get_pos()
                        if self.collide(pos):
                            self.__ready_to_click = True
                        else:
                            self.__ready_to_click = False
                    if event.type == self.game.it.MOUSEBUTTONUP:
                        pos = self.game.it.mouse.get_pos()
                        if self.collide(pos) and self.__ready_to_click:
                            self.__ready_to_click = False
                            self.click_func()
                if self.key is not None:
                    if event.type == self.game.it.KEYDOWN:
                        if event.key == self.key:
                            self.__ready_to_key = True
                        else:
                            self.__ready_to_key = False
                    if event.type == self.game.it.KEYUP:
                        if event.key == self.key and self.__ready_to_key:
                            self.__ready_to_key = False
                            self.click_func()


class TextRect(SimpleRect):
    def __init__(
        self, game: PyGame,
        text: str, pos: tuple, align: str = "center",
        font_family: str = "consolas", font_size: int = 100,
        fr_color: tuple = color.PaleGreen2, fr_alpha: float = 1,
        bg_color: tuple = color.cyan, bg_alpha: float = 0,
    ) -> None:
        # no super, since size is not calculated here
        self.game = game
        self.text = text
        self.pos = pos
        self.align = align
        self.font = self.game.it.font.SysFont(font_family, font_size)
        self.fr_color = fr_color
        self.fr_alpha = fr_alpha
        self.bg_color = bg_color
        self.bg_alpha = bg_alpha
        self.change_text(self.text)

    def change_text(self, text):
        self.text = text
        self.text = self.font.render(
            self.text, 1, [*self.fr_color, self.fr_alpha]
        )
        self.size = self.text.get_size()
        self.front = self.game.it.Surface(self.size).convert_alpha()
        self.front.fill([0, 0, 0, 0])
        self.front.set_alpha(int(256 * self.fr_alpha))
        self.front.blit(self.text, (0, 0))
        self.background = self.game.it.Surface(self.size)
        self.background.fill(self.bg_color)
        self.background.set_alpha(int(256 * self.bg_alpha))
        self.align_position()

    def collide(self, pos: tuple):
        return self.rect.collidepoint(*pos)

    def render(self):
        self.game.screen.blit(self.background, self.pos_align)
        self.game.screen.blit(self.front, self.pos_align)


class TextButton(TextRect):
    def __init__(
        self, game: PyGame,
        text: str, pos: tuple, align: str = "center",
        font_family: str = "consolas", font_size: int = 100,
        fr_color: tuple = color.PaleGreen2, fr_alpha: float = 1,
        bg_color: tuple = color.cyan, bg_alpha: float = 0,
        click_func: Optional[Callable] = None,
        key: Optional[int] = None,
        only_use_key: bool = False,
        activate_on_keydown: bool = False,
        long_update: bool = False,
    ):
        """
        only_use_key: if False, you can both use key or mouse; or you can only use key
        activate_on_keydown: if False, it will activate on keyup; or it will activate on keydown
        long_update: activate many times if press for a long time
        """
        super().__init__(
            game, text, pos, align, font_family,
            font_size, fr_color, fr_alpha, bg_color, bg_alpha
        )
        self.click_func = click_func
        self.key = key
        self.only_use_key = only_use_key
        self.activate_on_keydown = activate_on_keydown
        self.long_update = long_update
        self.long_press_frame = 0
        self.long_press_max = 25
        self.pressed = False
        self.__ready_to_click = False
        self.__ready_to_key = False

    def control_check(self):
        if self.click_func is not None:
            if self.activate_on_keydown and self.long_update:
                if self.pressed:
                    self.long_press_frame += 1
                else:
                    self.long_press_max = 25
                    self.long_press_frame = 0
                if self.long_press_frame >= self.long_press_max:
                    self.long_press_max = 10
                    self.long_press_frame = 0
                    self.click_func()

    def click_check(self, event: event.Event):
        if self.click_func is not None:

            if self.activate_on_keydown:
                if not self.only_use_key:
                    if event.type == self.game.it.MOUSEBUTTONDOWN:
                        pos = self.game.it.mouse.get_pos()
                        if self.collide(pos):
                            self.pressed = True
                            self.click_func()
                        else:
                            self.pressed = False
                    elif event.type == self.game.it.MOUSEBUTTONUP:
                        self.pressed = False
                if self.key is not None:
                    if event.type == self.game.it.KEYDOWN and event.key == self.key:
                        self.pressed = True
                        self.click_func()
                    if event.type == self.game.it.KEYUP and event.key == self.key:
                        self.pressed = False

            else:  # activate_on_keyup
                if not self.only_use_key:
                    if event.type == self.game.it.MOUSEBUTTONDOWN:
                        pos = self.game.it.mouse.get_pos()
                        if self.collide(pos):
                            self.__ready_to_click = True
                        else:
                            self.__ready_to_click = False
                    if event.type == self.game.it.MOUSEBUTTONUP:
                        pos = self.game.it.mouse.get_pos()
                        if self.collide(pos) and self.__ready_to_click:
                            self.__ready_to_click = False
                            self.click_func()
                if self.key is not None:
                    if event.type == self.game.it.KEYDOWN:
                        if event.key == self.key:
                            self.__ready_to_key = True
                        else:
                            self.__ready_to_key = False
                    if event.type == self.game.it.KEYUP:
                        if event.key == self.key and self.__ready_to_key:
                            self.__ready_to_key = False
                            self.click_func()


class RichRect:
    def __init__(
        self, game: PyGame,
        default_rect: SimpleRect,
        hover_rect: Optional[SimpleRect] = None,
        click_rect: Optional[SimpleRect] = None,
        collide_using_target: str = "self"
    ):
        """
        collide_using_target: "self", "default", "hover", "click"
        """
        self.game = game
        self.default_rect = default_rect
        self.hover_rect = default_rect if hover_rect is None else hover_rect
        self.click_rect = hover_rect if click_rect is None else click_rect
        self.collide_using_target = collide_using_target
        self.now_visible = "default"

    @property
    def now_rect(self):
        if self.now_visible == "default":
            return self.default_rect
        elif self.now_visible == "hover":
            return self.hover_rect
        elif self.now_visible == "click":
            return self.click_rect

    def collide(self, pos):
        if self.collide_using_target == "default":
            return self.default_rect.collide(pos)
        elif self.collide_using_target == "hover":
            return self.hover_rect.collide(pos)
        elif self.collide_using_target == "click":
            return self.click_rect.collide(pos)
        else:  # "self"
            return self.now_rect.collide(pos)

    def pre_click_check(self, event: event.Event):
        pos = self.game.it.mouse.get_pos()
        if event.type == self.game.it.MOUSEMOTION:
            if self.collide(pos):
                if self.game.it.mouse.get_pressed()[0]:
                    self.now_visible = "click"
                else:
                    self.now_visible = "hover"
            else:
                self.now_visible = "default"

    def render(self):
        self.now_rect.render()


class RichButton(RichRect):
    def __init__(
        self, game: PyGame,
        default_rect: SimpleRect,
        hover_rect: Optional[SimpleRect] = None,
        click_rect: Optional[SimpleRect] = None,
        collide_using_target: str = "self",
        click_func: Optional[Callable] = None,
        key: Optional[int] = None,
        only_use_key: bool = False,
        activate_on_keydown: bool = False,
        long_update: bool = False,
    ):
        """
        collide_using_target: "self", "default", "hover", "click"
        only_use_key: if False, you can both use key or mouse; or you can only use key
        activate_on_keydown: if False, it will activate on keyup; or it will activate on keydown
        long_update: activate many times if press for a long time
        """
        super().__init__(game, default_rect, hover_rect, click_rect, collide_using_target)
        self.click_func = click_func
        self.key = key
        self.only_use_key = only_use_key
        self.activate_on_keydown = activate_on_keydown
        self.long_update = long_update
        self.long_press_frame = 0
        self.long_press_max = 25
        self.__ready_to_click = False
        self.__ready_to_key = False

    def control_check(self):            
        if self.click_func is not None:
            if self.activate_on_keydown and self.long_update:
                if self.now_visible == "click":
                    self.long_press_frame += 1
                else:
                    self.long_press_max = 25
                    self.long_press_frame = 0
                if self.long_press_frame >= self.long_press_max:
                    self.long_press_max = 10
                    self.long_press_frame = 0
                    self.click_func()
                

    def click_check(self, event: event.Event):
        # don't forget this
        if not self.only_use_key:
            self.pre_click_check(event)
        
        if self.click_func is not None:

            if self.activate_on_keydown:
                if not self.only_use_key:
                    if event.type == self.game.it.MOUSEBUTTONDOWN:
                        pos = self.game.it.mouse.get_pos()
                        if self.collide(pos):
                            self.now_visible = "click"
                            self.click_func()
                        else:
                            self.now_visible = "default"
                    elif event.type == self.game.it.MOUSEBUTTONUP:
                        self.now_visible = "default"
                if self.key is not None:
                    if event.type == self.game.it.KEYDOWN and event.key == self.key:
                        self.now_visible = "click"
                        self.click_func()
                    if event.type == self.game.it.KEYUP and event.key == self.key:
                        self.now_visible = "default"

            else:  # activate_on_keyup
                if not self.only_use_key:
                    if event.type == self.game.it.MOUSEBUTTONDOWN:
                        pos = self.game.it.mouse.get_pos()
                        if self.collide(pos):
                            self.__ready_to_click = True
                        else:
                            self.__ready_to_click = False
                    if event.type == self.game.it.MOUSEBUTTONUP:
                        pos = self.game.it.mouse.get_pos()
                        if self.collide(pos) and self.__ready_to_click:
                            self.__ready_to_click = False
                            self.click_func()
                if self.key is not None:
                    if event.type == self.game.it.KEYDOWN:
                        if event.key == self.key:
                            self.now_visible = "click"
                            self.__ready_to_key = True
                        else:
                            self.now_visible = "default"
                            self.__ready_to_key = False
                    if event.type == self.game.it.KEYUP:
                        if event.key == self.key:
                            self.now_visible = "default"
                            if self.__ready_to_key:
                                self.__ready_to_key = False
                                self.click_func()


class ButtonAjustGroup:
    def __init__(
        self, game: PyGame,
        font_size: int = 30, pos: tuple = (0, 0),
        text: str = "", align: str = "left-up",
        left_img: str = "src/image/left_arrow.jpg",
        right_img: str = "src/image/right_arrow.jpg",
        default_value: int = 5, min_value: int = 1, max_value: int = 20,
        click_func: Optional[Callable] = None,
    ):
        self.game = game
        self.font_size = font_size
        self.pos = pos
        self.text = text
        self.num = default_value
        self.min_value = min_value
        self.max_value = max_value
        self.click_func = click_func

        self.text = TextRect(
            game, text, pos,
            align=align, font_size=font_size,
            fr_color=color.Red
        )
        x, y, _x, _y = self.text.rect
        self.left_rect = (x + _x, y, _x, _y)
        self.left = SimpleButton(
            game, size=(_y, _y), pos=(x + _x + 0.5 * _y, y),
            align=align, color=color.Red, image=left_img,
            click_func=self.click_left, activate_on_keydown=True,
            long_update=True
        )
        x, y, _x, _y = self.left.rect
        self.num_text = TextRect(
            game, str(self.num), pos=(x + _x + 0.5 * _y, y),
            align=align, font_size=font_size,
            fr_color=color.Red
        )
        x, y, _x, _y = self.num_text.rect
        self.right = SimpleButton(
            game, size=(_y, _y), pos=(x + _x + 0.5 * _y, y),
            align=align, color=color.Red, image=right_img,
            click_func=self.click_right, activate_on_keydown=True,
            long_update=True
        )

        self.render_list = [self.text, self.left, self.num_text, self.right]
        self.button_list = [self.left, self.right]

    def click_left(self):
        if self.num > self.min_value:
            self.num -= 1
        self.num_text.change_text(str(self.num))
        self.click_func()

    def click_right(self):
        if self.num < self.max_value:
            self.num += 1
        self.num_text.change_text(str(self.num))
        self.click_func()

    def render(self):
        for texture in self.render_list:
            texture.render()

    def control_check(self):
        for button in self.button_list:
            button.control_check()

    def click_check(self, event: event.Event):
        for button in self.button_list:
            button.click_check(event)
