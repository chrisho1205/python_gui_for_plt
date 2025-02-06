import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import os

print(f"當前工作目錄: {os.getcwd()}")

# 加载数据
loaded_data_y = np.load("./python_gui_for_realsense/old_data/foot_step_using_z_value_speed1.5/left_depth.npy", allow_pickle=True)
#print(loaded_data_y)
data=[]
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# 设置窗口大小
window_size = 3

# 平滑后的数据
smoothed_data_y = moving_average(loaded_data_y, window_size)

# 对 Y 轴数据取负号
#smoothed_data_y = -smoothed_data_y

# 找到y轴的局部最小值
local_min_y = argrelextrema(smoothed_data_y[:150], np.less,order=4)[0]

# 加载另一个数据
loaded_data_z = np.load('./python_gui_for_realsense/old_data/foot_step_using_z_value_speed1.5/right_depth.npy', allow_pickle=True)
for i in loaded_data_z:
    data.append(i)
    if len(data)>=3:
        smoothed_data_z = moving_average(data, window_size)

# 找到z轴的局部最大值
        local_max_z = argrelextrema(smoothed_data_z[:150], np.less,order=4)[0]

# 找到z轴的局部最大值与y轴的局部最小值差不到20个frame的点
common_indices = []
for i in local_max_z:
    for j in local_min_y:
        if abs(i - j) <= 5:
            common_indices.append((i, j))
print(common_indices)
# 绘制平滑后的数据
plt.plot(smoothed_data_y[:150],label="right")
plt.plot(smoothed_data_z[:150],label="left")
plt.scatter(local_min_y,smoothed_data_y[local_min_y], color='purple', label='Min Left', zorder=5)
plt.scatter(local_max_z,smoothed_data_z[local_max_z], color='green', label='Min right', zorder=5)
"""
fig, ax1 = plt.subplots()

# 绘制Y轴数据
ax1.plot(smoothed_data_y, 'r')
ax1.scatter(local_min_y, smoothed_data_y[local_min_y], color='green', label='Y minima')
ax1.set_xlabel("(Frame number)")
"""
"""
for idx, (i, j) in enumerate(common_indices):
    if idx == 0:  # 添加图例，只标注一次
        ax1.scatter(j, smoothed_data_y[j], color='green', label='Y ', zorder=5)
"""
"""
ax1.set_ylabel("Y (m)", color="r")
ax1.tick_params(axis="y", labelcolor="r")
ax1.legend(loc="upper left")

# 绘制Z轴数据
ax2 = ax1.twinx()
ax2.plot(smoothed_data_z, 'b')
ax2.scatter(local_max_z, smoothed_data_z[local_max_z], color='#FFA500', label='Z minima')
"""
"""
for idx, (i, j) in enumerate(common_indices):
    if idx == 0:  # 添加图例，只标注一次
        #ax1.scatter(j, smoothed_data_y[j], color='green', label='Y 最小值 (共通)', zorder=5)
        ax2.scatter(i, smoothed_data_z[i], color='#FFA500', label='Z ', zorder=5)
"""
"""
ax2.set_ylabel("Z (m)", color="b")
ax2.tick_params(axis="y", labelcolor="b")
ax2.legend(loc="upper right")

# 在满足条件的公共极值点上作图
for idx, (i, j) in enumerate(common_indices):
    if idx == 0:  # 添加图例，只标注一次
        ax1.scatter(j, smoothed_data_y[j], color='green', label='Y 最小值 (共通)', zorder=5)
        ax2.scatter(i, smoothed_data_z[i], color='#FFA500', label='Z 最大值 (共通)', zorder=5)
    else:
        ax1.scatter(j, smoothed_data_y[j], color='green', zorder=5)
        ax2.scatter(i, smoothed_data_z[i], color='#FFA500', zorder=5)

# 避免重复图例
"""
"""
handles, labels = fig.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
#fig.legend(by_label.values(), by_label.keys(), loc="lower center", ncol=2)
"""
plt.xlabel("frame")
plt.ylabel("Distance(m)")
plt.legend()
plt.show()
