import numpy as np
import matplotlib.pyplot as plt

loaded_data = np.load('C:\\Users\\chris\\Documents\\GitHub\\python_gui_for_realsesne0.2.0\\old_data\\left_degree121805dropfootstepokresult.npy', allow_pickle=True)
print(loaded_data)  # 輸出：[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# 設定窗口大小
window_size = 1 # 可根據需求調整

# 濾波後的數據
smoothed_data = moving_average(loaded_data, window_size)


plt.plot(smoothed_data )
loaded_data = np.load('C:\\Users\\chris\\Documents\\GitHub\\python_gui_for_realsesne0.2.0\\old_data\\right_degree121805dropfootokresult.npy', allow_pickle=True)
#print(loaded_data)  # 輸出：[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
smoothed_data = moving_average(loaded_data, window_size)

plt.plot(smoothed_data)

plt.show()
