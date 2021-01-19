class Scene():
    def __init__(self):
        pass
    
    def handle_events(self, events):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError

    def draw(self, window):
        raise NotImplementedError

class SceneManager(object):
    def __init__(self, InitScene):
        self.go_to(InitScene)

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self