import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

# 加载数据
loaded_data_z_right = np.load('./python_gui_for_realsense/right_distance.npy', allow_pickle=True)
loaded_data_z_left = np.load('./python_gui_for_realsense/left_distance.npy', allow_pickle=True)

# 数据长度和帧率
data_length = len(loaded_data_z_right)  # 200
fps = 10  # 10 FPS

# 生成时间刻度
time_seconds = data_length // fps  # 总时间为 20 秒
time_labels = [f"00:{str(i).zfill(2)}" for i in range(time_seconds + 1)]

# 每隔 10 个点对应一个秒
x_ticks = np.arange(0, data_length + 1, fps)

# 绘图
plt.plot(loaded_data_z_right, label="Right Foot Distance")
plt.plot(loaded_data_z_left, label="Left Foot Distance")

# 设置 X 轴
plt.xticks(ticks=x_ticks, labels=time_labels, rotation=45)
plt.xlabel("Time (mm:ss)")
plt.ylabel("Distance")
#plt.title("Foot Distance Over Time")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
