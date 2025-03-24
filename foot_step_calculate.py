import numpy as np
from scipy.signal import argrelextrema
import scipy.signal as signal
import os

# 設定參數
window_size = 5
fs = 100  # 取樣頻率 (Hz)
fc = 6    # 截止頻率 (Hz)
order = 1 # 一階濾波器

# 設計濾波器 (使用歸一化頻率)
b, a = signal.butter(order, fc / (fs / 2), btype='low', analog=False)

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

def threshold(data, dynamic_threshold, value):
    if len(data) > dynamic_threshold:
        max_threshold = max(data[-dynamic_threshold:])
        min_threshold = min(data[-dynamic_threshold:])
        average_threshold = (max_threshold + min_threshold) / 2
        return value < average_threshold
    return False

# 設定資料路徑
data_path = "C:\\Users\\chris\\Desktop\\test_data\\final_foot_step"
loaded_data_z_right = np.load(os.path.join(data_path, "left_depth.npy"), allow_pickle=True)
loaded_data_z_left = np.load(os.path.join(data_path, "right_depth.npy"), allow_pickle=True)

# 初始化變數
index_left = set()
index_right = set()

# 處理數據
data_length = len(loaded_data_z_left)
for i in range(data_length):
    left_depth_value_list = loaded_data_z_left[:i+1]
    right_depth_value_list = loaded_data_z_right[:i+1]
    
    smoothed_data_z_left = moving_average(left_depth_value_list, window_size)
    smoothed_data_z_right = moving_average(right_depth_value_list, window_size)
    
    local_min_z_left = argrelextrema(smoothed_data_z_left, np.less, order=5)[0]
    local_min_z_right = argrelextrema(smoothed_data_z_right, np.less, order=5)[0]
    
    if len(local_min_z_left) > 0:
        check_left = threshold(smoothed_data_z_left, 8, smoothed_data_z_left[local_min_z_left[-1]])
        if check_left and local_min_z_left[-1] not in index_left:
            index_left.add(local_min_z_left[-1])

    if len(local_min_z_right) > 0:
        check_right = threshold(smoothed_data_z_right, 8, smoothed_data_z_right[local_min_z_right[-1]])
        if check_right and local_min_z_right[-1] not in index_right:
            index_right.add(local_min_z_right[-1])

foot_step_count = len(index_left) + len(index_right)
print("foot_step_count:", foot_step_count)
