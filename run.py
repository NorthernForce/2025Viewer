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
colorizer = rs.colorizer()

colorizer.set_option(rs.option.visual_preset, 1)
colorizer.set_option(rs.option.min_distance, 0.25)
colorizer.set_option(rs.option.max_distance, 3)
colorizer.set_option(rs.option.color_scheme, 3) # black to white
config.enable_stream(rs.stream.depth, w, h, rs.format.z16, fps)
config.enable_stream(rs.stream.color, w, h, rs.format.rgb8, fps)

#align = rs.align(rs.stream.depth)
profile = pipe.start(config)

depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
print(f"scale: {depth_scale}m")

cs_video = CameraServer.putVideo("Video", w, h)
cs_depth = CameraServer.putVideo("Depth", w, h)

while True:
    frames = pipe.wait_for_frames()
    #frames = align.process(pipe.wait_for_frames())
    depth = frames.get_depth_frame()
    color = frames.get_color_frame()

    color_array = np.asanyarray(color.get_data())
    #depth_array = np.asanyarray(depth.get_data(), dtype=np.float64)
    dist_array = np.asanyarray(colorizer.colorize(depth).get_data())

    #print(dist_array.max(), "is max m")
    #print(depth_array)
    #print(dist_array)
    
    cs_video.putFrame(color_array)
    cs_depth.putFrame(cv2.convertScaleAbs(dist_array))
    continue
    #depth_array = cv2.convertScaleAbs(depth_array, alpha=0.03)
    #depth_array = cv2.bilateralFilter(depth_array, 10, 75, 75).astype(np.uint8)
    #depth_array = cv2.adaptiveThreshold(dist_array, 255,
    #    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2)
    #depth_array = np.where(thresh==-1, 65535, depth_array)
    #print(thresh)
    #depth_array = cv2.medianBlur(depth_array, 8)
    #cnt, hier = cv2.findContours(depth_array, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #depth_array = cv2.applyColorMap(depth_array, cv2.COLORMAP_JET)
    print(depth_array)
    #cv2.drawContours(color_array, cnt, -1, (0, 255, 0), 2)

    cs_video.putFrame(cv2.cvtColor(color_array, cv2.COLOR_RGB2BGR))
    cs_depth.putFrame(depth_array)
