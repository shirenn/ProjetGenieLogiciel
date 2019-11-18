#!/usr/bin/env python3


class Controller:
    
    def __init__(self, target=None):
        self._target = target
        self._actions = None
        
    def get_target():
        return self._target
        
    def set_actions(actions):
        self._actions = actions
        
    def execute():
        pass
        
        
class HomingController(Controller):
    
    def __init__(self, target=None, to_follow=None):
        super().__init__(self)
        self.__to_follow = to_follow
        self._actions = "Follow"
        
    def execute():
        self._target.execute("Follow")(self.__to_follow)
        
class KeyboardController(Controller):
    
    def __init__(self, target=None):
        super().__init__(self)
        self.correspondance = {}
        
    def add_event(event,action):
        self.coorespondance[event] = action
        
    def get_event():
        for event in pygame.event.get():
            for my_event in self.correspondance:
                if event == my_event:
                    return self.correspondance[my_event]
        return ("Nothing")
                    
    def execute():
        self._target.execute(get_event)()
        
class AutoPlay(Controller):
    
    def __init__(self, target=None, actions=[]):
        super().__init__(self)
        
    def execute():
        #TODO
        pass