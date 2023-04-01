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
      add_to_xxx(), del_xxx()

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

    def init(self):
        pass

    def event_deal(self, event: event.Event):
        pass

    def control_flow(self):
        pass

    def show(self):

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
                i.click_check(event)
            self.event_deal(event)

        self.control_flow()

        self._render()

        self.game.render_update()
        self.game.clock.tick(60)

    def _init(self):
        self._texture.clear()
        self._bind.clear()
        self.init()
        self.inited = True

    def del_render_list(self, object: Any) -> Any:
        self._texture.remove(object)

    def add_to_render_list(self, object: Any) -> None:
        '''
        object should have method .render()
        '''
        self._texture.append(object)

    def del_click_list(self, object) -> Any:
        self._bind.remove(object)

    def add_to_click_list(self, object) -> Any:
        '''
        object should have method .click_check(event)
        '''
        self._bind.append(object)

    def _render(self):
        for i in self._texture:
            i.render()


class SubPage(Page):
    """
    inherit this.

    you may need to overload:
      init(), event_deal(event), control_flow()

    you may need to use inside:
      add_to_xxx(), del_xxx()

    you must use outside:
      enter(), quit()

    you may use outside:
      rebind_mother_page()
    """

    def __init__(self, game: PyGame, state: StateMachine, mother_page: Page) -> None:
        super().__init__(game, state)
        self.mother_page = mother_page
        mother_page.daughters.append(self)
        self._ready = False
        self._del_mother_texture = []
    
    def rebind_mother_page(self, mother_page: Page):
        self.mother_page = mother_page
    
    def del_mother_visible(self, object):
        self._del_mother_texture.append(object)

    def enter(self):
        self._ready = True

    def quit(self):
        self._ready = False

    def _render(self):
        for i in self.mother_page._texture:
            if i not in self._del_mother_texture:
                i.render()
        for i in self._texture:
            i.render()