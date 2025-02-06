import pyrealsense2 as rs

# 創建管道
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# 開始串流
pipeline.start(config)

# 獲取一組幀
frames = pipeline.wait_for_frames()
color_frame = frames.get_color_frame()

# 獲取視頻流配置
color_profile = color_frame.get_profile()
video_stream_profile = rs.video_stream_profile(color_profile)
intrinsics = video_stream_profile.get_intrinsics()

# 輸出內參數
print(f"fx: {intrinsics.fx}")
print(f"fy: {intrinsics.fy}")
print(f"cx: {intrinsics.ppx}")
print(f"cy: {intrinsics.ppy}")

# 停止串流
pipeline.stop()