import sys
import time
import tkinter as tk

from PIL import Image, ImageTk
from cscore import CameraServer, VideoMode
import numpy as np
import pyrealsense2 as rs
# from ultralytics import YOLO

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
txt = tk.Label(root, text="Color + Depth")
txt.pack()
c_label = tk.Label(root)
c_label.pack()
d_label = tk.Label(root)
d_label.pack()

cs_video = CameraServer.putVideo("RealSense", w, h)

while True:
    frames = pipe.wait_for_frames()
    depth = frames.get_depth_frame()
    color = frames.get_color_frame()

    color_array = np.asanyarray(color.get_data())
    depth_array = np.asanyarray(depth.get_data(), dtype=np.float64)
    depth_array /= depth_array.max()

    c_img = Image.fromarray(color_array)
    d_img = Image.fromarray(depth_array*255)

    cs_video.putFrame(np.ascontiguousarray(color_array[..., ::-1]))
    
    c_imgtk = ImageTk.PhotoImage(c_img)
    d_imgtk = ImageTk.PhotoImage(d_img)
    c_label.config(image=c_imgtk)
    d_label.config(image=d_imgtk)
    
    root.update()