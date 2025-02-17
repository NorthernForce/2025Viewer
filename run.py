import sys
import time
import tkinter as tk

import numpy as np
from PIL import Image, ImageTk
# from ultralytics import YOLO
import pyrealsense2 as rs

# if len(sys.argv) != 2:
#     print(f"usage: {sys.argv[0]} path/to/model.pt")
#     sys.exit(1)

# model = YOLO(sys.argv[1])

w, h, fps = 640, 480, 30
pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, w, h, rs.format.z16, fps)
config.enable_stream(rs.stream.color, w, h, rs.format.rgb8, fps)

pipe.start(config)

root = tk.Tk()
while True:
    frames = pipe.wait_for_frames()
    depth = pipe.get_depth_frame()
    color = pipe.get_color_frame()
    img = Image.fromarray(np.asanyarray(color))

    imgtk = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=imgtk)
    label.pack()
    tk.update()