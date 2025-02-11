import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
window_size = 2
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

loaded_data_z_right = np.load("C:\\Users\\chris\\Documents\\GitHub\\test_data\\foot_step_distance80cm\\right_depth.npy", allow_pickle=True)
loaded_data_z_left = np.load("C:\\Users\\chris\\Documents\\GitHub\\test_data\\foot_step_distance80cm\\right_depth.npy", allow_pickle=True)
loaded_data_y_left = np.load("C:\\Users\\chris\\Documents\\GitHub\\test_data\\foot_step_distance80cm\\right_y.npy", allow_pickle=True)
#loaded_data_z_right=loaded_data_z_right[100:150]
#loaded_data_z_left=loaded_data_z_left[100:150]
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
    right_y_value_list=list(loaded_data_y_left[:i+1])
    #print( right_depth_value_list)
    # 卡尔曼滤波函数
    def kalman_filter(data, Q=1e-2, R=1e-2):
        n = len(data)
        x_hat = np.zeros(n)
        P = np.zeros(n)
        K = np.zeros(n)

        x_hat[0] = data[0]
        P[0] = 1

        for k in range(1, n):
            x_hat[k] = x_hat[k - 1]
            P[k] = P[k - 1] + Q

            K[k] = P[k] / (P[k] + R)
            x_hat[k] = x_hat[k] + K[k] * (data[k] - x_hat[k])
            P[k] = (1 - K[k]) * P[k]

        return x_hat
    check=False
    # 替换平滑滤波
    #smoothed_data_z_left = moving_average(left_depth_value_list,window_size)
    #smoothed_data_z_right = moving_average(right_depth_value_list,window_size)
    #smoothed_data_z_left = kalman_filter(smoothed_data_z_left)
    #smoothed_data_z_right = kalman_filter(smoothed_data_z_right)
    smoothed_data_z_left = kalman_filter(left_depth_value_list)
    smoothed_data_z_right = kalman_filter(right_depth_value_list)
    
    smoothed_data_y_right = kalman_filter(right_y_value_list)
    smoothed_data_y_right=-smoothed_data_y_right
    #smoothed_data_z_left = np.array(left_depth_value_list)
    #smoothed_data_z_right = np.array(right_depth_value_list)
    local_min_z_left = argrelextrema(smoothed_data_z_left , np.less,order=10)[0]
    local_min_z_right = argrelextrema(smoothed_data_z_right, np.less,order=10)[0]
    local_min_y_right = argrelextrema(smoothed_data_y_right, np.less,order=10)[0]
    local_max_z_left = argrelextrema(smoothed_data_z_left , np.greater,order=10)[0]
    local_max_z_right = argrelextrema(smoothed_data_z_right, np.greater,order=10)[0]
    local_max_y_right = argrelextrema(smoothed_data_y_right, np.greater,order=10)[0]
    """
    if len(local_min_z_left)>len(local_max_z_left):
        local_min_z_left_index=local_min_z_left[len(local_min_z_left)-1]
        smoothed_data_z_left=smoothed_data_z_left[ local_min_z_left_index:]
        smoothed_data_z_right=smoothed_data_z_right[ local_min_z_left_index:]
        """
    if len(local_max_z_left)>local_local_min_z_left_index:
        local_max_z_left_index=local_max_z_left[len(local_max_z_left)-1]
        right_distance_end_left=smoothed_data_z_left[local_max_z_left_index]
        right_distance_end_right= smoothed_data_z_right[local_max_z_left_index]
        frame_right=local_max_z_left_index
    if len(local_min_z_left) > local_local_min_z_left_index  :
        """
        if len(local_min_z_left)>len(local_max_z_left):
            print(len(local_min_z_left))
            local_min_z_left_index=local_min_z_left[len(local_min_z_left)]
            print(local_min_z_left_index)
            """
        
        local_min_z_left_index=local_min_z_left[len(local_min_z_left)-1]
        right_distance_start_left=smoothed_data_z_left[local_min_z_left_index]
        right_distance_start_right= smoothed_data_z_right[local_min_z_left_index]
        print(local_min_z_left_index)
        frame_left=local_min_z_left_index
    """"
    if len(local_min_z_left) > local_local_min_z_left_index and len(local_max_z_right)==0:
        local_min_z_left_index=local_min_z_left[len(local_min_z_left)-1]
        smoothed_data_z_left=smoothed_data_z_left[local_min_z_left_index:]
        smoothed_data_z_right= smoothed_data_z_right[local_min_z_left_index:]
        print(local_min_z_left_index)
        frame_left=local_min_z_left_index
    """
    if len(local_min_z_left) > local_local_min_z_left_index and len(local_max_z_left)>local_local_min_z_left_index and frame_left>frame_right:
    # print("start_time")
        #print(smoothed_data_z_left[frame_left])
        #print(smoothed_data_z_right[frame_left])
        #print(frame_left)
        #print("==================")
        #print("end_time")
        #print(smoothed_data_z_left[frame_left])
        #print(smoothed_data_z_right[frame_left])
        #print(frame_right)
        #print("-------------------")

        left_foot_distance= right_distance_end_left- right_distance_start_left
        right_foot_distance= right_distance_end_right- right_distance_start_right

        left_distance=abs(left_foot_distance)+abs(right_foot_distance)
        #print(right_distance_end_left)
        #print(right_distance_start_left)
        #print(right_distance_end_right)
        #print(right_distance_start_right)
        #print(left_foot_distance)
        #print(right_foot_distance)
        #if(left_distance>0.9):
        print("left_distance")
        print(left_distance)
        local_local_min_z_left_index=len(local_min_z_left)
        #print("left_distance")
        distance_left.append(left_distance)
        #print(left_distance)
        #print("left_distance2")
        #print(right_foot_distance)
        #print("======================")
        foot_step_count=left_distance
        distance_left_value=distance_left_value+left_distance
        distance_left_count+=1
   
        #label.setFootstep( foot_step_count,1)
    #local_min_z_left = np.array([])
    #local_max_z_left= np.array([])
   
    #========================================================
    if len(local_min_z_right)>local_local_min_z_right_index and  len(local_max_z_right)>0:
        #print(len(local_min_z_right))
        local_min_z_right_index=local_min_z_right[len(local_min_z_right)-1]
        #print(local_min_z_right_index)
        left_distance_start_right=smoothed_data_z_right[local_min_z_right_index]
        left_distance_start_left= smoothed_data_z_left[local_min_z_right_index]
    if len(local_max_z_right)>local_local_min_z_right_index:
        local_max_z_right_index=local_max_z_right[len(local_max_z_right)-1]
        left_distance_end_right=smoothed_data_z_right[local_max_z_right_index]
        left_distance_end_left= smoothed_data_z_left[local_max_z_right_index]
    if len(local_min_z_right)>local_local_min_z_right_index and len(local_max_z_right)>local_local_min_z_right_index:
        right_foot_distance= left_distance_end_right-  left_distance_start_right
        left_foot_distance= left_distance_end_left-  left_distance_start_left
        
        #print(right_foot_distance)
        #print(left_foot_distance)
        right_distance=abs(left_foot_distance)+abs(right_foot_distance)
        #if(right_distance>0.9):
        print("right_distance")
        print(right_distance)
        distance_right.append(right_distance)
        distance_right_value=distance_right_value+right_distance
        distance_right_count+=1
        local_local_min_z_right_index=len(local_min_z_right)
        foot_step_left=right_distance
   
            # label.setFootstep( foot_step_count,2)
        #local_min_z_right = np.array([])
        #local_max_z_right= np.array([])
        
       #plt.plot(smoothed_data_z_left, label="Left Foot Distance")
        plt.plot(smoothed_data_y_right, label="Left Foot Distance")
        plt.plot(smoothed_data_z_right, label="Right Foot Distance")
        #plt.scatter(local_max_z_left, smoothed_data_z_left[local_max_z_left], color='purple', label='Max Left', zorder=5)
        #plt.scatter(local_min_z_left, smoothed_data_z_left[local_min_z_left], color='green', label='Min Left', zorder=5)
        plt.scatter(local_max_y_right, smoothed_data_y_right[local_max_y_right], color='purple', label='Max Left', zorder=5)
        plt.scatter(local_max_z_right, smoothed_data_z_right[local_max_z_right], color='green', label='Min Left', zorder=5)

        # 生成时间刻度
        data_length = len(smoothed_data_z_left)  # 平滑数据的长度
        fps = 10  # 每秒帧数
        x_ticks = np.arange(0, data_length, fps)  # 每秒一个 tick

        # 只生成与 ticks 数量匹配的时间标签
        time_labels = [f"00:{str(i//fps).zfill(2)}" for i in x_ticks]

        # 设置 X 轴时间刻度
        plt.xticks(ticks=x_ticks, labels=time_labels, rotation=45)

        # 设置 X 轴时间刻度
        plt.xticks(ticks=x_ticks, labels=time_labels, rotation=45)
        plt.xlabel("Time (mm:ss)")
        plt.ylabel("Distance")
        plt.title("Foot Distance Over Time")
        
        plt.grid()
        plt.pause(0.01)  # 暂停以更新图像
# 保存距离数据
plt.legend()
plt.grid()
np.save("left_distance.npy", distance_left)
np.save("right_distance.npy", distance_right)
print(local_max_y_right)
print(local_max_z_right)
plt.ioff()  # 關閉互動模式
plt.show()  # 顯示最終結果