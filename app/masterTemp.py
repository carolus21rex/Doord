import os
import cv2
import random

import keyboard

from app.deploy import deploy
import time
from tkinter import Tk, Canvas


class App:
    def __init__(self, master):
        self.canvas = Canvas(master, width=600, height=600)
        self.canvas.pack()

        self.box = self.canvas.create_rectangle(50, 50, 500, 500, fill="red")

    def flip_color(self, state):
        color = "green" if not state else "red"
        self.canvas.itemconfig(self.box, fill=color)


def init_gui():
    root = Tk()
    app = App(root)
    return app, root


def master():
    cap = cv2.VideoCapture(0)
    red = True
    gui, root = init_gui()
    try:
        # Initialize the AI model
        model = deploy.init_model(True)

        while True:
            ret, frame = cap.read()

            det = deploy.pass_model(model, frame)

            if det:
                red = False

            if keyboard.is_pressed(' '):
                red = True
            gui.flip_color(red)

            time.sleep(0.1)

            root.update()

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        # Release the video capture object
        cap.release()

        # Destroy all OpenCV windows
        cv2.destroyAllWindows()

        # Quit the GUI
        root.quit()


if __name__ == "__main__":
    master()
