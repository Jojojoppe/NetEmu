import threading
import cv2
import numpy as np

class GuiThread(threading.Thread):
    def __init__(self, nodes):
        threading.Thread.__init__(self, name='GuiThread')
        self.nodes = nodes
        self.running = True

        # GUI FPS
        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)

        # GUI data
        self.window_name = "NetEmu"
        self.gui_data = np.zeros([600,600,3])

    def mouseCallback(self, event, x, y, flags, param):
        self.gui_data[y,x,:] = [255,255,255]

    def run(self):
        # Render gui
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouseCallback)
        while self.running:
            cv2.imshow(self.window_name, self.gui_data)
            cv2.waitKey(self.FPS_MS)
        cv2.destroyAllWindows()

    def stop(self):
        self.running = False