import threading
import numpy as np
import pygame

class GuiThread(threading.Thread):
    def __init__(self, nodes):
        threading.Thread.__init__(self, name='GuiThread')
        self.nodes = nodes
        self.running = True

        pygame.init()
        self.fpsClock = pygame.time.Clock()
        self.window = pygame.display.set_mode((400, 300), 0, 32)
        pygame.display.set_caption('NetEmu Server')

    def run(self):
        # Render gui
        while self.running:
            self.window.fill((255, 255, 255))
            
            pygame.display.update()
            self.fpsClock.tick(30)

        pygame.quit()

    def stop(self):
        self.running = False