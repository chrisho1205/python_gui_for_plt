import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import os

# 設定參數
fs = 20   # 取樣頻率 (Hz)
fc = 5    # 截止頻率 (Hz)
order = 1 # 一階濾波器
window_size = 5  # 滑動平均窗口

# 設計低通濾波器
b, a = signal.butter(order, fc / (fs / 2), btype='low', analog=False)

def lowpass_filter(data, b, a):
    """應用 IIR 低通濾波"""
    return signal.filtfilt(b, a, data)  # 使用 filtfilt 避免相位延遲

def moving_average(data, window_size):
    """滑動平均濾波"""
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

def threshold(data, dynamic_threshold, value):
    """動態閾值判斷"""
    if len(data) > dynamic_threshold:
        max_threshold = max(data[-dynamic_threshold:])
        min_threshold = min(data[-dynamic_threshold:])
        average_threshold = (max_threshold + min_threshold) / 2
        return value < average_threshold, max_threshold, min_threshold, average_threshold
    return False, None, None, None

# 設定資料路徑
data_path = "C:\\Users\\chris\\Desktop\\test_data\\final_foot_step"
loaded_data_z_right = np.load(os.path.join(data_path, "right_depth.npy"), allow_pickle=True)
loaded_data_z_left = np.load(os.path.join(data_path, "left_depth.npy"), allow_pickle=True)

# 應用低通濾波
filtered_data_z_right = lowpass_filter(loaded_data_z_right, b, a)
filtered_data_z_left = lowpass_filter(loaded_data_z_left, b, a)

# 初始化變數
index_left = set()  
index_right = set()
foot_step_count = 0

max_threshold_values_left = []
min_threshold_values_left = []
avg_threshold_values_left = []

max_threshold_values_right = []
min_threshold_values_right = []
avg_threshold_values_right = []

# 設定動態繪圖
plt.ion()  # 開啟即時繪圖模式
fig, ax = plt.subplots(figsize=(10, 5))

# 處理數據
data_length = len(filtered_data_z_left)
for i in range(data_length):
    left_depth_value_list = list(filtered_data_z_left[:i+1])
    right_depth_value_list = list(filtered_data_z_right[:i+1])
    
    smoothed_data_z_left = moving_average(left_depth_value_list, window_size)
    smoothed_data_z_right = moving_average(right_depth_value_list, window_size)
    
    # 取得局部最小值
    local_min_z_left = signal.argrelextrema(smoothed_data_z_left, np.less, order=3)[0]
    local_min_z_right = signal.argrelextrema(smoothed_data_z_right, np.less, order=3)[0]
    
    # 閾值判斷
    if len(local_min_z_left) > 0:
        check_left, max_threshold_left, min_threshold_left, avg_threshold_left = threshold(
            smoothed_data_z_left, 10, smoothed_data_z_left[local_min_z_left[-1]]
        )
    else:
        check_left = False
        max_threshold_left, min_threshold_left, avg_threshold_left = None, None, None

    if len(local_min_z_right) > 0:
        check_right, max_threshold_right, min_threshold_right, avg_threshold_right = threshold(
            smoothed_data_z_right, 10, smoothed_data_z_right[local_min_z_right[-1]]
        )
    else:
        check_right = False
        max_threshold_right, min_threshold_right, avg_threshold_right = None, None, None

    # 記錄 threshold 數值
    max_threshold_values_left.append(max_threshold_left if max_threshold_left is not None else None)
    min_threshold_values_left.append(min_threshold_left if min_threshold_left is not None else None)
    avg_threshold_values_left.append(avg_threshold_left if avg_threshold_left is not None else None)

    max_threshold_values_right.append(max_threshold_right if max_threshold_right is not None else None)
    min_threshold_values_right.append(min_threshold_right if min_threshold_right is not None else None)
    avg_threshold_values_right.append(avg_threshold_right if avg_threshold_right is not None else None)
    
    if check_left and local_min_z_left[-1] not in index_left:
        index_left.add(local_min_z_left[-1])

    if check_right and local_min_z_right[-1] not in index_right:
        index_right.add(local_min_z_right[-1])

    # **動態繪圖**
    ax.cla()  # 清除舊圖

    # 畫出當前數據
    ax.plot(smoothed_data_z_right, label="Right Foot Distance", color='blue')
    ax.plot(smoothed_data_z_left, label="Left Foot Distance", color='red')

    # 畫出局部最小值
    ax.scatter(list(index_right), [smoothed_data_z_right[j] for j in index_right if j < len(smoothed_data_z_right)], color='green', label='Min Right', zorder=5)
    ax.scatter(list(index_left), [smoothed_data_z_left[j] for j in index_left if j < len(smoothed_data_z_left)], color='blue', label='Min Left', zorder=5)

    # 畫出 Threshold 線條
    ax.plot(max_threshold_values_left, linestyle='dashed', color='red', label="Max Threshold Left")
    ax.plot(max_threshold_values_right, linestyle='dashed', color='red', label="Max Threshold Right")

    ax.plot(min_threshold_values_left, linestyle='dashed', color='blue', label="Min Threshold Left")
    ax.plot(min_threshold_values_right, linestyle='dashed', color='blue', label="Min Threshold Right")

    ax.plot(avg_threshold_values_left, linestyle='dashed', color='yellow', label="Average Threshold Left")
    ax.plot(avg_threshold_values_right, linestyle='dashed', color='black', label="Average Threshold Right")

    # 設定圖例與標題
    ax.legend()
    ax.set_title(f"Dynamic Footstep Detection (Frame {i + 1})")

    # 更新畫面
    plt.pause(0.01)

foot_step_count = len(index_left) + len(index_right)
print("foot_step_count:", foot_step_count)

plt.ioff()  # 關閉即時繪圖模式
plt.show()
