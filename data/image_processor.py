import os
import time
import tkinter as tk
import random
from shutil import move
import utils.WindowsUtil as wu
from PIL import Image, ImageDraw
import cv2

displayImage = None
wholeBox = True
clickLoc = [None, None]
prevLoc = [None, None]
labels = []
root = wu.create_gui()
imagePointer = None
progress = 0


def save_progress(file_name, progress):
    """
    This function writes the current progress to a file.

    :param file_name: the name of the file in which to save the progress.
    :param progress: the current progress.
    """
    with open(file_name, "w") as file:
        file.write(f'{progress}')


def read_progress(file_name):
    """
    This function reads a single integer from a file.

    :param file_name: the name of the file from which to read the integer.
    :return: the integer read from the file.
    """
    with open(file_name, "r") as file:
        return int(file.readline().strip())


def clear_image(label):
    global displayImage, wholeBox, labels, imagePointer
    displayImage = Image.open(imagePointer)
    displayImage = displayImage.resize((350, 350))
    labels = []
    wholeBox = True
    wu.update_image(label, displayImage)


def get_random_jpg_from_folder(folder_path):
    """
    This function takes path to a folder as input and returns the path to a random jpeg file.
    If there are no jpeg files in the folder, it returns None.
    """
    jpg_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]

    if not jpg_files:  # no jpg files in the folder
        return None

    random_jpg = random.choice(jpg_files)

    return os.path.join(folder_path, random_jpg)


def get_next_image(labelz):
    global displayImage, imagePointer, progress, labels
    if imagePointer is not None:
        move(imagePointer, os.path.join(os.getcwd(), "images", f"image_{progress:03d}.jpg"))
        with open(os.path.join(os.getcwd(), "labels", f"image_{progress:03d}.txt"), "w") as file:
            for label in labels:
                file.write(f'{label}')

    imagePointer = get_random_jpg_from_folder("./preprocessed_images")

    progress += 1
    labels = []
    displayImage = Image.open(imagePointer)
    displayImage = displayImage.resize((350, 350))
    wu.update_image(labelz, displayImage)


def quit_ip(root):
    root.destroy()


def parse_loc():
    global clickLoc, prevLoc
    x1, y1 = prevLoc
    x2, y2 = clickLoc
    if x1 > x2:
        temp = x1
        x1 = x2
        x2 = temp
    if y1 > y2:
        temp = y1
        y1 = y2
        y2 = temp

    return [x1, y1, x2, y2]


def addBox(loc):
    global displayImage
    x1, y1, x2, y2 = map(float, loc.split(', '))
    draw = ImageDraw.Draw(displayImage)
    draw.rectangle(((x1, y1), (x2, y2)), outline="green")


def check_clicks(root, lc, tb):
    global clickLoc, prevLoc, labels, wholeBox

    if clickLoc != prevLoc:
        wholeBox = not wholeBox
        if wholeBox:
            loc = parse_loc()
            addBox(f"{loc[0]*350-25}, {loc[1]*350-75}, {loc[2]*350-25}, {loc[3]*350-75}")
            label = "0"
            for l in loc:
                label += f", {l / 350}"
            label += "\n"
            labels.append(label)
            wu.update_image(lc[0], displayImage)
        prevLoc[0] = clickLoc[0]
        prevLoc[1] = clickLoc[1]

    wu.write_to_textbox(tb, labels)

    root.after(50, check_clicks, root, lc, tb)


def main():
    global clickLoc, progress
    progress = read_progress("progress.ini")
    labelContainer = [None]  # mutable container
    wu.add_button(root, "next_image", lambda: get_next_image(labelContainer[0]))
    wu.add_button(root, "clear_image", lambda: clear_image(labelContainer[0]))
    labelContainer[0] = wu.add_image(root, clickLoc)
    text_box = wu.add_text_box(root, 5)
    wu.add_button(root, "Quit", lambda: quit_ip(root))
    root.after(50, check_clicks, root, labelContainer, text_box)
    root.mainloop()
    save_progress("progress.ini", progress)


if __name__ == '__main__':
    main()
