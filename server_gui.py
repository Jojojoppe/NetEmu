import threading
import numpy as np
import sdl2.ext as sdl

class GuiThread(threading.Thread):
    def __init__(self, nodes):
        threading.Thread.__init__(self, name='GuiThread')
        self.nodes = nodes
        self.running = True

        # GUI data
        self.gui_data = np.zeros([600,600,3])
        self.zoom_level = 1.0

        sdl.init()
        self.window = sdl.Window("NetEmu Server", size=(800, 600))
        self.renderer = sdl.Renderer(self.window)

    def run(self):
        # Render gui
        self.window.show()
        self.renderer.clear(0)
        while self.running:
            events = sdl.get_events()
            self.renderer.present()
        sdl.quit()

    def stop(self):
        self.running = False