import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import scipy.signal as signal
import os
window_size =5
fs = 20  # 取樣頻率 (Hz)
fc = 3  # 截止頻率 (Hz)
order = 1 # 一階濾波器

# 設計濾波器 (使用歸一化頻率)
b, a = signal.butter(order, fc / (fs / 2), btype='low', analog=False)
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')
def lowpass_filter(data, b, a):
    """應用 IIR 低通濾波"""
    return signal.filtfilt(b, a, data)  # 使用 filtfilt 避免相位延遲
def threshold(data, dynamic_threshold, value):
    """動態閾值判斷"""
    if len(data) > dynamic_threshold:
        max_threshold = max(data[-dynamic_threshold:])
        min_threshold = min(data[-dynamic_threshold:])
        average_threshold = (max_threshold + min_threshold) / 2
        return value < average_threshold, max_threshold, min_threshold, average_threshold
    return False, None, None, None
data_path = "C:\\Users\\chris\\Desktop\\test_data\\final_foot_step"
loaded_data_z_right = np.load(os.path.join(data_path, "right_depth.npy"), allow_pickle=True)
loaded_data_z_left = np.load(os.path.join(data_path, "left_depth.npy"), allow_pickle=True)
loaded_data_z_right = lowpass_filter(loaded_data_z_right, b, a)
loaded_data_z_left = lowpass_filter(loaded_data_z_left, b, a)

frame_left=0
frame_right=0
distance_left=[]
distance_right=[]
distance_right_value=0
distance_left_value=0
distance_right_count=0
distance_left_count=0
local_local_min_z_right_index=0
local_local_min_z_left_index=0
for i in range(len(loaded_data_z_left)):
    left_depth_value_list=list(loaded_data_z_left[:i+1])
    right_depth_value_list=list(loaded_data_z_right[:i+1])

    # 替换平滑滤波
    smoothed_data_z_left = moving_average(left_depth_value_list,window_size)

    smoothed_data_z_right = moving_average(right_depth_value_list,window_size)

    local_min_z_left = argrelextrema(smoothed_data_z_left , np.less,order=5)[0]
    local_min_z_right = argrelextrema(smoothed_data_z_right, np.less,order=5)[0]
    
    local_max_z_left = argrelextrema(smoothed_data_z_left , np.greater,order=5)[0]
    local_max_z_right = argrelextrema(smoothed_data_z_right, np.greater,order=5)[0]
   
    
    if len(local_max_z_left)>local_local_min_z_left_index:
        local_max_z_left_index=local_max_z_left[len(local_max_z_left)-1]
        right_distance_end_left=smoothed_data_z_left[local_max_z_left_index]
        right_distance_end_right= smoothed_data_z_right[local_max_z_left_index]
        frame_right=local_max_z_left_index
    if len(local_min_z_left) > local_local_min_z_left_index  :
      
        
        local_min_z_left_index=local_min_z_left[len(local_min_z_left)-1]
        right_distance_start_left=smoothed_data_z_left[local_min_z_left_index]
        right_distance_start_right= smoothed_data_z_right[local_min_z_left_index]
        #print(local_min_z_left_index)
        frame_left=local_min_z_left_index

    if len(local_min_z_left) > local_local_min_z_left_index and len(local_max_z_left)>local_local_min_z_left_index and frame_left>frame_right:
   

        left_foot_distance= right_distance_end_left- right_distance_start_left
        right_foot_distance= right_distance_end_right- right_distance_start_right
        left_distance=abs(left_foot_distance)+abs(right_foot_distance)
        print("left_distance")
        print(left_distance)
        local_local_min_z_left_index=len(local_min_z_left)
        distance_left.append(left_distance)
        foot_step_count=left_distance
        distance_left_value=distance_left_value+left_distance
        distance_left_count+=1
   
       
   
    #========================================================
    if len(local_min_z_right)>local_local_min_z_right_index and  len(local_max_z_right)>0:
      
        local_min_z_right_index=local_min_z_right[len(local_min_z_right)-1]
        
        left_distance_start_right=smoothed_data_z_right[local_min_z_right_index]
        left_distance_start_left= smoothed_data_z_left[local_min_z_right_index]
    if len(local_max_z_right)>local_local_min_z_right_index:
        local_max_z_right_index=local_max_z_right[len(local_max_z_right)-1]
        left_distance_end_right=smoothed_data_z_right[local_max_z_right_index]
        left_distance_end_left= smoothed_data_z_left[local_max_z_right_index]
    if len(local_min_z_right)>local_local_min_z_right_index and len(local_max_z_right)>local_local_min_z_right_index:
        right_foot_distance= left_distance_end_right-  left_distance_start_right
        left_foot_distance= left_distance_end_left-  left_distance_start_left
        
        
        right_distance=abs(left_foot_distance)+abs(right_foot_distance)
       
        print("right_distance")
        print(right_distance)
        distance_right.append(right_distance)
        distance_right_value=distance_right_value+right_distance
        distance_right_count+=1
        local_local_min_z_right_index=len(local_min_z_right)
        foot_step_left=right_distance
   
        plt.plot(smoothed_data_z_right, label="Left Foot Distance", color='blue')
        plt.plot(smoothed_data_z_left, label="left Foot Degree", color='red')
        
        plt.scatter(local_max_z_left, smoothed_data_z_left[local_max_z_left], color='purple', label='Max Left', zorder=5)
        plt.scatter(local_min_z_left, smoothed_data_z_left[local_min_z_left], color='green', label='Min Left', zorder=5)

        # 生成时间刻度
        data_length = len(smoothed_data_z_left)  # 平滑数据的长度
        fps = 10  # 每秒帧数
        x_ticks = np.arange(0, data_length, fps)  # 每秒一个 tick

        # 只生成与 ticks 数量匹配的时间标签
        time_labels = [f"00:{str(i//fps).zfill(2)}" for i in x_ticks]
#plt.legend()
        # 设置 X 轴时间刻度
plt.xticks(ticks=x_ticks, labels=time_labels, rotation=45)

# 设置 X 轴时间刻度
plt.xticks(ticks=x_ticks, labels=time_labels, rotation=45)
plt.xlabel("Time (mm:ss)")
plt.ylabel("Distance/degree")
#plt.title("Foot Distance Over Time")

plt.grid()
#plt.pause(0.01)  # 暂停以更新图像
# 保存距离数据


print(local_max_z_right)
print(local_max_z_right)
plt.ioff()  # 關閉互動模式
plt.show()  # 顯示最終結果