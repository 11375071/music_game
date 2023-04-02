from typing import List, Any
from pygame import event
from utils.define import PyGame, StateMachine


# wait for future use (refactor)
class Page:
    """
    inherit this.

    you may need to overload:
      init(), event_deal(event), control_flow()

    you may need to use inside:
      add_to_xxx(), del_from_xxx()

    you must use outside:
      show()
    """

    def __init__(self,  game: PyGame, state: StateMachine) -> None:
        self.game = game
        self.state = state
        self.inited = False
        self.in_daughter = False
        self.daughters: List[SubPage] = []
        self._texture: list = []
        self._bind: list = []
        self.frame = 0

    def init(self) -> None:
        pass

    def event_deal(self, event: event.Event) -> None:
        pass

    def control_flow(self) -> None:
        pass

    def show(self) -> None:

        self.frame += 1

        self.in_daughter = False
        for i in self.daughters:
            if i._ready:
                self.in_daughter = True
                i.show()
                break

        if self.in_daughter:
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

        # if self.frame % 60 == 0:
        #     print(self.frame, len(self._texture), len(self._bind))

        if self.frame >= 5184000:
            self.frame = 0

        self.game.render_update()
        self.game.clock.tick(60)

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
      init(), event_deal(event), control_flow()

    you may need to use inside:
      add_to_xxx(), del_from_xxx()

    you must use outside:
      enter(), quit()
    """

    def __init__(
        self, game: PyGame,
        state: StateMachine, mother_page: Page,
        need_mother_texture: bool = False,
    ) -> None:
        super().__init__(game, state)
        self.mother_page = mother_page
        mother_page.daughters.append(self)
        self._ready = False
        self.need_mother_texture = need_mother_texture
        self._del_mother_texture = []

    def del_from_mother_visible(self, object) -> None:
        self._del_mother_texture.append(object)

    def enter(self) -> None:
        self._ready = True

    def quit(self) -> None:
        self._ready = False

    def _render(self) -> None:
        if self.need_mother_texture:
            for i in self.mother_page._texture:
                if i not in self._del_mother_texture:
                    i.render()
        for i in self._texture:
            i.render()
