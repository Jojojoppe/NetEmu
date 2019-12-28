import threading
import numpy as np
import pygame

class GuiThread(threading.Thread):
    def __init__(self, nodes):
        threading.Thread.__init__(self, name='GuiThread')
        self.nodes = nodes
        self.running = True

        self.width = 800
        self.height = 600
        pygame.init()
        self.fpsCam = pygame.time.Clock()
        self.window = pygame.display.set_mode((self.width, self.height), 0, 32)

        self.zoom = 1.0
        self.zoom_speed = 1.1

    def run(self):
        # Render gui
        while self.running:
            self.window.fill((255, 255, 255))

            for nodename, node in self.nodes.items():
                x,y = self.get_screen_position(node.position)
                pygame.draw.circle(self.window, (255, 0, 0), (int(x), int(y)), 2, 0)
                pygame.draw.circle(self.window, (0, 0, 255), (int(x), int(y)), int(self.zoom*1.5), 1)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    self.zoom *= self.zoom_speed
                    print("Zoom: ", self.zoom)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                    self.zoom /= self.zoom_speed
                    print("Zoom: ", self.zoom)

            pygame.display.update()
            self.fpsCam.tick(30)
        pygame.quit()

    def stop(self):
        self.running = False

    def get_screen_position(self, pos):
        x, y = pos
        wx = ((self.zoom*x)+1)*(self.width/2)
        wy = ((self.zoom*y)+1)*(self.height/2)
        return wx,wy