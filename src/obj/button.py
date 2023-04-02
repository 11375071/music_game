from pygame import event
from numpy import ndarray
import utils.color as color
from utils.define import PyGame
from pygame.surface import Surface
from typing import Callable, Optional, Union, Tuple, List, Any
from obj.property import KeyCheckProperty, PositionProperty, ImageProperty


class SimpleRect(ImageProperty, PositionProperty):
    """
    a simple rect, with solid color or picture
    """
    def __init__(
        self, game: PyGame,
        size: tuple, pos: tuple, align: str = "center",
        color: tuple = color.PaleGreen2, alpha: float = 1,
        image: Optional[Union[str, Surface, Tuple[Surface, ndarray]]] = None,
        collide_ignore_transparent: bool = False, already_scaled: bool = False,
    ) -> None:
        """
        Initial a simple rect, with solid color or picture (Surface or path).

        Args:
            size: (x_width, y_height), float number allowed
            pos: (x_pos, y_pos), float number allowed
            align: "center", "left-up", "left-down", "right-up", "right-down" to anchor with `pos`
            color: (R, G, B), range in 0 ~ 255. Validate when `image` is None
            alpha: 0.0 ~ 1.0, 0.0 is transparent, 1.0 is opaque
            image: None (use solid color), str (picture path), Surface (pygame.surface.Surface), Tuple[Surface, ndarry] (mpimg.imread, see `collide_ignore_transparent`). Surface and Tuple is faster than str.
            collide_ignore_transparent: if is True and `image` is not None, `collide()` will ignore area where picture's alpha == 0. If enabled, use Tuple[Surface, ndarry] as `image` will load faster
            already_scaled: if is True and `image` is not None, SimpleRect will no longer change image's size in order to load faster
            
        Methods:
            collide(pos: tuple): detect whether pos is on the
            render(): blit on PyGame.screen
        """
        self.game = game
        self.size = size
        self.pos = pos
        self.align = align
        self.color = color
        self.alpha = alpha
        self.image = image
        self.collide_ignore_transparent = collide_ignore_transparent
        self.already_scaled = already_scaled

        self.original_image: Optional[Surface] = None
        self.change_image()
        self.align_position()

    def collide(self, pos: tuple) -> bool:
        if self.collide_ignore_transparent and self.collide_detect_used_image is not None:
            if not self.collide_rect.collidepoint(*pos):
                return False
            return self.collide_detect_used_image[
                int(pos[1] / self.size[1] * self.collide_detect_used_image.shape[0])
            ][
                int(pos[0] / self.size[0] * self.collide_detect_used_image.shape[1])
            ][-1] != 0
        else:
            return self.collide_rect.collidepoint(*pos)

    def render(self) -> None:
        self.game.screen.blit(self.image, self.pos_align)


class SimpleButton(SimpleRect, KeyCheckProperty):
    def __init__(
        self, game: PyGame,
        size: tuple, pos: tuple, align: str = "center",
        color: tuple = color.PaleGreen2, alpha: float = 1,
        image: Optional[Union[str, Surface, Tuple[Surface, ndarray]]] = None,
        collide_ignore_transparent: bool = False, already_scaled: bool = False,
        click_func: Optional[Callable] = None,
        key: Optional[int] = None,
        only_use_key: bool = False,
        activate_on_keydown: bool = False,
        press_update: bool = False,
    ) -> None:
        """
        Args:
            only_use_key: if False, you can both use key or mouse; otherwise you can only use key
            activate_on_keydown: if False, it will activate on keyup; otherwise it will activate on keydown
            press_update: activate many times if press for a long time (only worked when activate_on_keydown is enabled)
        """
        super().__init__(game, size, pos, align, color, alpha, image, collide_ignore_transparent, already_scaled)
        self.click_func = click_func
        self.key = key
        self.only_use_key = only_use_key
        self.activate_on_keydown = activate_on_keydown
        self.press_update = press_update

        self.now_press_state: str = ""
        self.long_press_frame: int = 0
        self.long_press_max: int = 0
        self.ready_to_click: bool = False
        self.ready_to_key: bool = False


class TextRect(PositionProperty):
    def __init__(
        self, game: PyGame,
        text: str, pos: tuple, align: str = "center",
        font_family: str = "consolas", font_size: int = 100,
        fr_color: tuple = color.PaleGreen2, fr_alpha: float = 1,
        bg_color: tuple = color.cyan, bg_alpha: float = 0,
    ) -> None:
        """
        size is automatic generated on text size
        """
        self.game = game
        self.text = text
        self.pos = pos
        self.align = align
        self.font = self.game.it.font.SysFont(font_family, font_size)
        self.fr_color = fr_color
        self.fr_alpha = fr_alpha
        self.bg_color = bg_color
        self.bg_alpha = bg_alpha

        self.original_image: Optional[Surface] = None
        self.change_text(self.text)

    def change_text(self, text) -> None:
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

    def collide(self, pos: tuple) -> bool:
        return self.collide_rect.collidepoint(*pos)

    def render(self) -> None:
        self.game.screen.blit(self.background, self.pos_align)
        self.game.screen.blit(self.front, self.pos_align)


class TextButton(TextRect, KeyCheckProperty):
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
        press_update: bool = False,
    ) -> None:
        """
        Args:
            only_use_key: if False, you can both use key or mouse; otherwise you can only use key
            activate_on_keydown: if False, it will activate on keyup; otherwise it will activate on keydown
            press_update: activate many times if press for a long time (only worked when activate_on_keydown is enabled)
        """
        super().__init__(
            game, text, pos, align, font_family,
            font_size, fr_color, fr_alpha, bg_color, bg_alpha
        )
        self.click_func = click_func
        self.key = key
        self.only_use_key = only_use_key
        self.activate_on_keydown = activate_on_keydown
        self.press_update = press_update

        self.now_press_state: str = ""
        self.long_press_frame: int = 0
        self.long_press_max: int = 0
        self.ready_to_click: bool = False
        self.ready_to_key: bool = False


class MultipleTextButton(SimpleButton):
    def __init__(
        self, game: PyGame,
        size: tuple, pos: tuple, align: str = "center",
        color: tuple = color.PaleGreen2, alpha: float = 1,
        image: Optional[Union[str, Surface, Tuple[Surface, ndarray]]] = None,
        collide_ignore_transparent: bool = False, already_scaled: bool = False,
        click_func: Optional[Callable] = None,
        key: Optional[int] = None,
        only_use_key: bool = False,
        activate_on_keydown: bool = False,
        press_update: bool = False
    ) -> None:
        """
        Args:
            only_use_key: if False, you can both use key or mouse; otherwise you can only use key
            activate_on_keydown: if False, it will activate on keyup; otherwise it will activate on keydown
            press_update: activate many times if press for a long time (only worked when activate_on_keydown is enabled)
        """
        super().__init__(
            game, size, pos, align,
            color, alpha, image,
            collide_ignore_transparent, already_scaled,
            click_func, key, only_use_key,
            activate_on_keydown, press_update
        )

    def append_text(self, object: TextRect) -> None:
        """
        Args:
            object: position must be relative
        """
        self.image.blit(object.background, object.pos_align)
        self.image.blit(object.front, object.pos_align)


class RichRect:
    def __init__(
        self, game: PyGame,
        default_rect: SimpleRect,
        hover_rect: Optional[SimpleRect] = None,
        click_rect: Optional[SimpleRect] = None,
        collide_using_target: str = "self"
    ) -> None:
        """
        Args:
            collide_using_target: "self", "default", "hover", "click"
        """
        self.game = game
        self.default_rect = default_rect
        self.hover_rect = default_rect if hover_rect is None else hover_rect
        self.click_rect = hover_rect if click_rect is None else click_rect
        self.collide_using_target = collide_using_target

        self.now_press_state: str = "default"

    @property
    def now_rect(self) -> Surface:
        if self.now_press_state == "default":
            return self.default_rect
        elif self.now_press_state == "hover":
            return self.hover_rect
        elif self.now_press_state == "click":
            return self.click_rect
        else:
            return self.default_rect

    def collide(self, pos) -> bool:
        if self.collide_using_target == "default":
            return self.default_rect.collide(pos)
        elif self.collide_using_target == "hover":
            return self.hover_rect.collide(pos)
        elif self.collide_using_target == "click":
            return self.click_rect.collide(pos)
        else:  # "self"
            return self.now_rect.collide(pos)

    def render(self) -> None:
        self.now_rect.render()


class RichButton(RichRect, KeyCheckProperty):
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
        press_update: bool = False,
    ) -> None:
        """
        Args:
            collide_using_target: "self", "default", "hover", "click"
            only_use_key: if False, you can both use key or mouse; otherwise you can only use key
            activate_on_keydown: if False, it will activate on keyup; otherwise it will activate on keydown
            press_update: activate many times if press for a long time (only worked when activate_on_keydown is enabled)
        """
        super().__init__(game, default_rect, hover_rect, click_rect, collide_using_target)
        self.click_func = click_func
        self.key = key
        self.only_use_key = only_use_key
        self.activate_on_keydown = activate_on_keydown
        self.press_update = press_update

        self.long_press_frame: int = 0
        self.long_press_max: int = 25
        self.ready_to_click: bool = False
        self.ready_to_key: bool = False


class ButtonAjustGroup:
    def __init__(
        self, game: PyGame,
        font_size: int = 30, pos: tuple = (0, 0),
        text: str = "", align: str = "left-up",
        left_img: str = "src/image/left_arrow.jpg",
        right_img: str = "src/image/right_arrow.jpg",
        default_value: int = 5, min_value: int = 1, max_value: int = 20,
        click_func: Optional[Callable] = None,
    ) -> None:
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
        x, y, _x, _y = self.text.collide_rect
        self.left_rect = (x + _x, y, _x, _y)
        self.left = SimpleButton(
            game, size=(_y, _y), pos=(x + _x + 0.5 * _y, y),
            align=align, color=color.Red, image=left_img,
            click_func=self.click_left, activate_on_keydown=True,
            press_update=True
        )
        x, y, _x, _y = self.left.collide_rect
        self.num_text = TextRect(
            game, str(self.num), pos=(x + _x + 0.5 * _y, y),
            align=align, font_size=font_size,
            fr_color=color.Red
        )
        x, y, _x, _y = self.num_text.collide_rect
        self.right = SimpleButton(
            game, size=(_y, _y), pos=(x + _x + 0.5 * _y, y),
            align=align, color=color.Red, image=right_img,
            click_func=self.click_right, activate_on_keydown=True,
            press_update=True
        )

        self.render_list = [self.text, self.left, self.num_text, self.right]
        self.button_list = [self.left, self.right]

    def click_left(self) -> None:
        if self.num > self.min_value:
            self.num -= 1
        self.num_text.change_text(str(self.num))
        self.click_func()

    def click_right(self) -> None:
        if self.num < self.max_value:
            self.num += 1
        self.num_text.change_text(str(self.num))
        self.click_func()

    def render(self) -> None:
        for texture in self.render_list:
            texture.render()

    def control_check(self) -> bool:
        activate = False
        for button in self.button_list:
            if button.control_check():
                activate = True
        return activate

    def event_check(self, event: event.Event) -> bool:
        activate = False
        for button in self.button_list:
            if button.event_check(event):
                activate = True
        return activate
