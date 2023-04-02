from typing import List, Any
from pygame import event
from utils.define import PyGame, StateMachine


# wait for future use (refactor)
class Page:
    """
    inherit this.

    you may need to overload:
      `init(self)`, `event_deal(self, event)`, `control_flow(self)`

    you may need to use inside:
      `self.add_to_xxx(object)`, `self.del_from_xxx(object)`, `self.game`, `self.state`, `self.inited`

    you must use outside:
      `page_obj.show()`
    """

    def __init__(
        self,
        game: PyGame, state: StateMachine,
        fps: int = 60,
    ) -> None:
        self.game = game
        self.state = state
        self.fps = fps

        self.inited = False
        self._in_daughter = False
        self._daughters: List[SubPage] = []
        self._texture: list = []
        self._bind: list = []
        self._frame = 0

    def init(self) -> None:
        pass

    def event_deal(self, event: event.Event) -> None:
        pass

    def control_flow(self) -> None:
        pass

    def show(self) -> None:

        self._frame += 1

        self._in_daughter = False
        for i in self._daughters:
            if i._ready:
                self._in_daughter = True
                i.show()
                break

        if self._in_daughter:
            return

        if not self.inited:
            self._init()

        for event in self.game.it.event.get():
            if event.type == self.game.it.QUIT:
                self.state.quit = True
            for i in self._bind:
                i.event_check(event)
            self.event_deal(event)

        for i in self._bind:
            i.control_check()

        self.control_flow()

        self._render()

        # if self._frame % self.fps == 0:
        #     print(self._frame, len(self._texture), len(self._bind))

        if self._frame >= 86400 * self.fps:
            self._frame = 0

        self.game.render_update()
        self.game.clock.tick(self.fps)

    def _init(self) -> None:
        self._texture.clear()
        self._bind.clear()
        self.init()
        self.inited = True

    def _render(self) -> None:
        for i in self._texture:
            i.render()

    def del_from_render_list(self, object: Any) -> Any:
        self._texture.remove(object)

    def add_to_render_list(self, object: Any) -> None:
        '''
        object must have method `render()`
        '''
        self._texture.append(object)

    def del_from_check_list(self, object) -> None:
        self._bind.remove(object)

    def add_to_check_list(self, object) -> Any:
        '''
        object must have method `event_check(event)` and `control_check()`
        '''
        self._bind.append(object)


class SubPage(Page):
    """
    inherit this.

    you may need to overload:
      `init(self)`, `event_deal(self, event)`, `control_flow(self)`

    you may need to use inside:
      `self.add_to_xxx(object)`, `self.del_from_xxx(object)`, `self.game`, `self.state`, `self.inited`, `self.mother_page`

    you must use outside:
      `page_obj.enter()`, `page_obj.quit()`
    """

    def __init__(
        self,
        game: PyGame, state: StateMachine,
        mother_page: Page,
        need_mother_texture: bool = False,
        fps: int = 60,
    ) -> None:
        super().__init__(game, state, fps)
        self.mother_page = mother_page
        self.mother_page._daughters.append(self)
        self._ready = False
        self._need_mother_texture = need_mother_texture
        self._del_mother_texture = []

    def del_from_mother_visible(self, object) -> None:
        self._del_mother_texture.append(object)

    def enter(self) -> None:
        self._ready = True

    def quit(self) -> None:
        self._ready = False

    def _render(self) -> None:
        if self._need_mother_texture:
            for i in self.mother_page._texture:
                if i not in self._del_mother_texture:
                    i.render()
        for i in self._texture:
            i.render()
