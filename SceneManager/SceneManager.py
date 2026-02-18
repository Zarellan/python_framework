class SceneManager:
    current_scene = None

    @classmethod
    def load_scene(cls, new_scene):
        # Destroy old scene
        if cls.current_scene:
            cls.current_scene.destroy()
        
        cls.current_scene = new_scene
        cls.current_scene.start()

    @classmethod
    def handle_events(cls, events):
        if cls.current_scene:
            cls.current_scene.handle_events(events)

    @classmethod
    def update(cls):
        if cls.current_scene:
            cls.current_scene.update()

    @classmethod
    def render(cls):
        if cls.current_scene:
            cls.current_scene.render()
