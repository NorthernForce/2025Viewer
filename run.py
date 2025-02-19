from cscore import CameraServer
import numpy as np
import pyrealsense2 as rs
import cv2
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

cs_video = CameraServer.putVideo("Video", w, h)
cs_depth = CameraServer.putVideo("Depth", w, h)

while True:
    frames = pipe.wait_for_frames()
    depth = frames.get_depth_frame()
    color = frames.get_color_frame()

    color_array = np.asanyarray(color.get_data())
    depth_array = np.asanyarray(depth.get_data(), dtype=np.float64)

    depth_array = cv2.convertScaleAbs(depth_array, alpha=0.03)
    depth_array = cv2.applyColorMap(depth_array, cv2.COLORMAP_JET)

    cv2.imshow("Color", color_array)
    cv2.imshow("Depth Map", depth_array)
    cv2.waitKey(1)

    cs_video.putFrame(cv2.cvtColor(color_array, cv2.COLOR_RGB2BGR))
    cs_depth.putFrame(depth_array)