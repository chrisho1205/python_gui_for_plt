import pyrealsense2 as rs
import numpy as np
import cv2

# 初始化 RealSense 管道
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # 启用深度流
pipeline.start(config)

# 定义目标区域（例如，左上角和右下角坐标）
roi_x_min, roi_y_min = 100, 100  # 区域左上角
roi_x_max, roi_y_max = 200, 200  # 匂域右下角

try:
    while True:
        # 获取深度帧
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue

        # 深度图转 NumPy 数组
        depth_image = np.asanyarray(depth_frame.get_data())

        # 相机内参
        profile = pipeline.get_active_profile()
        intr = profile.get_stream(rs.stream.depth).as_video_stream_profile().get_intrinsics()
        fx, fy, cx, cy = intr.fx, intr.fy, intr.ppx, intr.ppy

        # 生成点云
        h, w = depth_image.shape
        x = np.tile(np.arange(w), (h, 1))
        y = np.tile(np.arange(h).reshape(-1, 1), (1, w))
        z = depth_image / 1000.0  # 深度值单位从毫米转为米

        # 三维点云坐标
        x = (x - cx) * z / fx
        y = (y - cy) * z / fy

        # 提取目标区域的深度图数据
        roi_depth = depth_image[roi_y_min:roi_y_max, roi_x_min:roi_x_max]
        roi_x = x[roi_y_min:roi_y_max, roi_x_min:roi_x_max]
        roi_y = y[roi_y_min:roi_y_max, roi_x_min:roi_x_max]
        roi_z = z[roi_y_min:roi_y_max, roi_x_min:roi_x_max]

        # 梯度计算
        dzdx = np.gradient(roi_z, axis=1)
        dzdy = np.gradient(roi_z, axis=0)

        # 法向量计算
        normals = np.zeros((roi_y_max - roi_y_min, roi_x_max - roi_x_min, 3), dtype=np.float32)
        normals[..., 0] = -dzdx  # n_x
        normals[..., 1] = -dzdy  # n_y
        normals[..., 2] = 1.0    # n_z
        norm = np.linalg.norm(normals, axis=2, keepdims=True)
        normals /= norm  # 归一化

        # 可视化 Z 轴方向法向量
        z_normals = normals[..., 2]  # 提取 n_z 分量

        # 归一化并转换为 uint8 类型
        z_normals_visual = ((z_normals - z_normals.min()) / (z_normals.max() - z_normals.min()) * 255).astype(np.uint8)

        # 在原图中显示目标区域法向量
        depth_image_colored = cv2.applyColorMap(depth_image.astype(np.uint8), cv2.COLORMAP_JET)
        z_normals_colored = cv2.applyColorMap(z_normals_visual, cv2.COLORMAP_JET)

        # 将法向量图像叠加到原深度图像上
        depth_image_colored[roi_y_min:roi_y_max, roi_x_min:roi_x_max] = z_normals_colored

        # 显示结果
        cv2.imshow('Depth with Normals', depth_image_colored)

        # 按下 'q' 退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # 停止管道
    pipeline.stop()
