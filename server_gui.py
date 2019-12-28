import threading
import numpy as np
import pygame

class GuiThread(threading.Thread):
    def __init__(self, nodes, config):
        threading.Thread.__init__(self, name='GuiThread')
        self.nodes = nodes
        self.config = config
        self.running = True

        self.width = int(config.get('gui', 'window_size', fallback=400))
        self.height = self.height
        pygame.init()
        self.fpsCam = pygame.time.Clock()
        self.window = pygame.display.set_mode((self.width, self.height), 0, 32)

        self.zoom = float(config.get('gui', 'zoom', fallback='1.0'))
        self.zoom_speed = float(config.get('gui', 'zoom_speed', fallback='1.1'))
        self.tx_line = int(config.get('gui', 'tx_line', fallback='-40'))

    def run(self):
        # Render gui
        while self.running:
            self.window.fill((255, 255, 255))

            for nodename, node in self.nodes.items():
                x,y = self.get_screen_position(node.position)
                pygame.draw.circle(self.window, (255, 0, 0), (int(x), int(y)), 2, 0)

                # Draw -40dBm line
                d = node.calc_dist(self.tx_line)
                pygame.draw.circle(self.window, (0, 0, 255), (int(x), int(y)), int(self.get_screen_length(d)), 1)

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
        wx = ((self.zoom*x)+1)*(self.height/2)
        wy = ((self.zoom*y)+1)*(self.width/2)
        return wx,wy

    def get_screen_length(self, length):
        return ((self.zoom*length))*(self.height/2)