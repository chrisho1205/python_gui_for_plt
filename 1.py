import cv2
import mediapipe as mp
import pyrealsense2 as rs
import numpy as np
import math
from collections import deque

# 初始化 MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# 初始化 RealSense 相机
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # 添加深度流
pipeline.start(config)

# 移动平均滤波器（平滑角度变化）
fpa_left_history = deque(maxlen=5)  # 存储最近 5 帧的左脚角度
fpa_right_history = deque(maxlen=5)  # 存储最近 5 帧的右脚角度

def calculate_fpa(heel, toe):
    """计算 2D 脚的进展角 (Foot Progression Angle)"""
    dx, dy = toe[0] - heel[0], toe[1] - heel[1]
    angle = math.degrees(math.atan2(dy, dx))  # 计算角度
    return angle

def get_depth_coordinates(depth_frame, x, y):
    """获取 RealSense 深度信息 (x, y) 对应的实际 3D 位置"""
    depth = depth_frame.get_distance(int(x), int(y))  # 获取深度 (单位: 米)
    return depth

while True:
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()

    if not color_frame or not depth_frame:
        continue

    img = np.asanyarray(color_frame.get_data())
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # MediaPipe 处理
    results = pose.process(img_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # 获取左右脚 2D 坐标
        left_heel_2d = (landmarks[mp_pose.PoseLandmark.LEFT_HEEL].x * img.shape[1],
                        landmarks[mp_pose.PoseLandmark.LEFT_HEEL].y * img.shape[0])
        left_toe_2d = (landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x * img.shape[1],
                       landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y * img.shape[0])

        right_heel_2d = (landmarks[mp_pose.PoseLandmark.RIGHT_HEEL].x * img.shape[1],
                         landmarks[mp_pose.PoseLandmark.RIGHT_HEEL].y * img.shape[0])
        right_toe_2d = (landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x * img.shape[1],
                        landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].y * img.shape[0])

        # 计算 FPA（2D）
        fpa_left = calculate_fpa(left_heel_2d, left_toe_2d)
        fpa_right = calculate_fpa(right_heel_2d, right_toe_2d)

        # 平滑数据（移动平均）
        fpa_left_history.append(fpa_left)
        fpa_right_history.append(fpa_right)
        fpa_left_smooth = np.mean(fpa_left_history)
        fpa_right_smooth = np.mean(fpa_right_history)

        # 获取 3D 深度信息
        left_heel_depth = get_depth_coordinates(depth_frame, *left_heel_2d)
        left_toe_depth = get_depth_coordinates(depth_frame, *left_toe_2d)
        right_heel_depth = get_depth_coordinates(depth_frame, *right_heel_2d)
        right_toe_depth = get_depth_coordinates(depth_frame, *right_toe_2d)

        # 计算 3D 角度（如果深度数据有效）
        if left_heel_depth > 0 and left_toe_depth > 0:
            dz = left_toe_depth - left_heel_depth
            fpa_left_3d = math.degrees(math.atan2(dz, left_toe_2d[0] - left_heel_2d[0]))
        else:
            fpa_left_3d = fpa_left_smooth  # 用 2D 角度代替

        if right_heel_depth > 0 and right_toe_depth > 0:
            dz = right_toe_depth - right_heel_depth
            fpa_right_3d = math.degrees(math.atan2(dz, right_toe_2d[0] - right_heel_2d[0]))
        else:
            fpa_right_3d = fpa_right_smooth  # 用 2D 角度代替

        # 在影像上显示结果
        cv2.putText(img, f'Left FPA: {fpa_left_3d:.2f}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(img, f'Right FPA: {fpa_right_3d:.2f}', (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # 在图像上绘制关键点
        cv2.circle(img, tuple(map(int, left_heel_2d)), 5, (255, 0, 0), -1)
        cv2.circle(img, tuple(map(int, left_toe_2d)), 5, (0, 255, 0), -1)
        cv2.circle(img, tuple(map(int, right_heel_2d)), 5, (255, 0, 0), -1)
        cv2.circle(img, tuple(map(int, right_toe_2d)), 5, (0, 255, 0), -1)

        # 绘制脚的方向箭头
        cv2.arrowedLine(img, tuple(map(int, left_heel_2d)), tuple(map(int, left_toe_2d)), (0, 255, 255), 3)
        cv2.arrowedLine(img, tuple(map(int, right_heel_2d)), tuple(map(int, right_toe_2d)), (0, 255, 255), 3)

    # 显示影像
    cv2.imshow("Foot Progression Angle (3D)", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

pipeline.stop()
cv2.destroyAllWindows()
