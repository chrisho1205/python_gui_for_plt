import pyrealsense2 as rs
import numpy as np
import cv2
import math
import mediapipe as mp
import matplotlib.pyplot as  plt
import time
def draw_custom_landmarks(image, landmarks, selected_points, custom_connections):
    h, w, _ = image.shape
    
    # 繪製連線
    for start_idx, end_idx in custom_connections:
        start = landmarks.landmark[start_idx]
        end = landmarks.landmark[end_idx]
        
        # 確保點的可見性
        if start.visibility > 0.3 and end.visibility > 0.3:
            start_point = (int(start.x * w), int(start.y * h))
            end_point = (int(end.x * w), int(end.y * h))
            cv2.line(image, start_point, end_point, (0, 255, 0), 2)
    
    # 繪製點
    
    for idx in selected_points:
        point = landmarks.landmark[idx]
        if point.visibility > 0.3:
            point_coords = (int(point.x * w), int(point.y * h))
            cv2.circle(image, point_coords, 5, (0, 0, 255), -1)
    
def calculate_roi_mediapipe_calibrate(depth_image,x,y):
    h, w = 480,640
    ROI_width=20
    x_calibrate=((x-321.1242370605469)*depth_image.get_distance(x, y))/610.4790649414062
    y_calibrate=((y-246.25962829589844)*depth_image.get_distance(x, y))/610.4264526367188
    #print(x)
    roi_x = max(int(x -ROI_width / 2.0), 0)
    roi_y = max(int(y - ROI_width / 2.0), 0)
    roi_x2 = min(roi_x +ROI_width, w)
    roi_y2 = min(roi_y + ROI_width, h)
    #x_calibrate=(x-320)/100
    #y_calibrate=(y-240)/100
    #print(x_calibrate)
    #print("x")
    #print(x_calibrate)
    #print(depth_image.get_distance(x, y))
    depth_roi_sum = 0
    depth_roi_count = 0

    for y_ in range(roi_y, roi_y2):
        for x_ in range(roi_x, roi_x2):
            z_value =  depth_image.get_distance(x_, y_)
            if z_value:
                depth_roi_sum += z_value
                depth_roi_count += 1
    #print(depth_roi_sum)
    if depth_roi_count > 0:
        avg_depth = depth_roi_sum / depth_roi_count
        #avg_depth = depth_image.get_distance(x, y)
    else:
        avg_depth = 0  # 如果 ROI 中沒有有效的深度數據，設為 0
    roi_depth=avg_depth
    
    #avg_depth= math.sqrt(roi_depth**2-((x_calibrate)**2+(y_calibrate)**2))
    #avg_depth= math.sqrt((depth_image.get_distance(x, y)**2)-(((x-320)**2)+((y-240)**2)))
    #print(avg_depth)
    return x_calibrate,y_calibrate,avg_depth
def calculate_roi_mediapipe( depth_image,x,y):
    h, w = 480,640
    ROI_width=10
    # 計算 ROI 範圍
    roi_x = max(int(x -ROI_width / 2.0), 0)
    roi_y = max(int(y - ROI_width / 2.0), 0)
    roi_x2 = min(roi_x +ROI_width, w)
    roi_y2 = min(roi_y + ROI_width, h)
    #print(roi_x,roi_x2,roi_y,roi_y2)
    # 計算 ROI 中的平均深度值
    depth_roi_sum = 0
    depth_roi_count = 0

    for y_ in range(roi_y, roi_y2):
        for x_ in range(roi_x, roi_x2):
            z_value =  depth_image.get_distance(x_, y_)
            if z_value:
                depth_roi_sum += z_value
                depth_roi_count += 1
    #print(depth_roi_sum)
    if depth_roi_count > 0:
        avg_depth = depth_roi_sum / depth_roi_count
        #avg_depth = depth_image.get_distance(x, y)
    else:
        avg_depth = 0  # 如果 ROI 中沒有有效的深度數據，設為 0
    roi_depth=avg_depth
    
    return avg_depth
       


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)
align_to = rs.stream.color
align = rs.align(align_to)
fourcc =cv2.VideoWriter_fourcc(*'XVID')
out=cv2.VideoWriter('output.avi',fourcc,30.0,(640,480))
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
    
x_value_list=[]
y_value_list=[]
line_degree=[]
depth_value_mediapipe_calibrate_list=[]
# 初始化绘图工具
mp_drawing = mp.solutions.drawing_utils
try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)   
        depth_frame =  aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        rgb_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        
        line1=[]
        line2=[]
        left_node_1=23
        left_node_2=29
        left_node_3=31
        right_node_1=24
        right_node_2=30
        right_node_3=32
        left_node_4=29
        right_node_4=30
        line_right_shoulder=[]
        line_right_hip=[]
        line_right_knee=[]
        right_x_value_list=[]
        right_y_value_list=[]
        right_line_degree=[]
        right_depth_value_mediapipe_calibrate_list=[]
        left_x_value_list=[]
        left_y_value_list=[]
        left_line_degree=[]
        left_depth_value_mediapipe_calibrate_list=[]
        foot_step_time=[]
        foot_step_count=0
        results = pose.process(rgb_image)
        if results.pose_landmarks:
            for index,landmark in enumerate(results.pose_landmarks.landmark):
    # 获取每个关键点的置信度
                confidence = landmark.visibility

    # 过滤置信度低于 0.5 的关键点
                if confidence > 0.3:
                    h, w, _ = color_image.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    #cv2.circle(color_image, (x, y), 5, (0, 255, 0), -1)
                    if index==0:
                       
                        if(x>=0 and x<640 and y<480 and y>=0):
                            #depth_value_mediapipe=calculate_roi_mediapipe(depth_frame,x,y)
                            #x_value,y_value,depth_value_mediapipe_calibrate=calculate_roi_mediapipe_calibrate(depth_frame,x,y)
                            #x_value_list.append(x_value)
                            #y_value_list.append(y_value)
                            #depth_value_mediapipe_calibrate_list.append(depth_value_mediapipe_calibrate)
                            print("nose")
                           
                            #print(depth_value_mediapipe_calibrate)
                        # gravity  
                        """
                        if index==11:  
                            if(x>=0 and x<640 and y<480 and y>=0):
                                line1 = [x, y]       
                            #print(depth_value_mediapipe_calibrate)
                        if index==12:
                            
                            if(x>=0 and x<640 and y<480 and y>=0):
                                line2 = [x, y]
                            #depth_value_mediapipe_calibrate=calculate_roi_mediapipe_calibrate(depth_frame,x,y)
                        if line1 and line2:
                            x_gravity=int((line1[0]+line2[0])/2)
                            y_gravity=int((line1[1]+line2[1])/2)
                            x_value,y_value,depth_value_mediapipe_calibrate=calculate_roi_mediapipe_calibrate(depth_frame,x_gravity,y_gravity)
                            x_value_list.append(x_value)
                            y_value_list.append(y_value)
                            depth_value_mediapipe_calibrate_list.append(depth_value_mediapipe_calibrate) 
                        """
                    
                    if index==left_node_1:
                                    
                        if(x>=0 and x<640 and y<480 and y>=0):
                            x_value_left_shoulder,y_value_left_shoulder,depth_value_mediapipe_calibrate_left_shoulder=calculate_roi_mediapipe_calibrate(depth_frame,x,y)     
                            line_left_shoulder= [x_value_left_shoulder,y_value_left_shoulder]
                            #y_left_value_degree=y
                        #print(depth_value_mediapipe_calibrate)
                    if index==right_node_1:
                        if(x>=0 and x<640 and y<480 and y>=0):
                            #line_right_shoulder = [x, y]
                            x_value_right_shoulder,y_value_right_shoulder,depth_value_mediapipe_calibrate_right_shoulder=calculate_roi_mediapipe_calibrate(depth_frame,x,y) 
                            line_right_shoulder = [x_value_right_shoulder,y_value_right_shoulder] 
                            #y_right_value_degree=y 
                    if index==left_node_2:
                        if(x>=0 and x<640 and y<480 and y>=0):
                            line_left_hip = [x, y]
                            x_value_left_hip,y_value_left_hip,depth_value_mediapipe_calibrate_left_hip=calculate_roi_mediapipe_calibrate(depth_frame,x,y)  
                            line_left_hip = [x_value_left_hip,y_value_left_hip]   
                            #x_left_value_degree=x                             
                    if index==right_node_2:
                        if(x>=0 and x<640 and y<480 and y>=0):
                            line_right_hip = [x, y]
                            x_value_right_hip,y_value_right_hip,depth_value_mediapipe_calibrate_right_hip=calculate_roi_mediapipe_calibrate(depth_frame,x,y)  
                            line_right_hip = [x_value_right_hip,y_value_right_hip]
                            #x_right_value_degree=x
                    if index==left_node_3:
                        if(x>=0 and x<640 and y<480 and y>=0):
                            #line_left_knee = [x, y]
                            x_value_left_knee,y_value_left_knee,depth_value_mediapipe_calibrate_left_knee=calculate_roi_mediapipe_calibrate(depth_frame,x,y) 
                            line_left_knee = [x_value_left_knee,y_value_left_knee] 
                    if index==right_node_3:
                        if(x>=0 and x<640 and y<480 and y>=0):
                            #line_right_knee = [x, y]
                            x_value_right_knee,y_value_right_knee,depth_value_mediapipe_calibrate_right_knee=calculate_roi_mediapipe_calibrate(depth_frame,x,y)  
                            line_right_knee = [x_value_right_knee,y_value_right_knee]
                    if left_node_4>0 and right_node_4>0:
                        if index==left_node_4:
                            if(x>=0 and x<640 and y<480 and y>=0):
                            #line_right_knee = [x, y]
                                x_value_left_heel,y_value_left_heel,depth_value_mediapipe_calibrate_left_heel=calculate_roi_mediapipe_calibrate(depth_frame,x,y)  
                                line_left_heel = [x_value_left_heel,y_value_left_heel]
                        if index==right_node_4:
                            if(x>=0 and x<640 and y<480 and y>=0):
                                x_value_right_heel,y_value_right_heel,depth_value_mediapipe_calibrate_right_heel=calculate_roi_mediapipe_calibrate(depth_frame,x,y)  
                                line_right_heel = [x_value_right_heel,y_value_right_heel]
                                           
                    if line_right_shoulder and  line_right_hip and line_right_knee and line_left_shoulder and  line_left_hip and line_left_knee and line_left_heel and line_right_heel:
                        print("foot_step")
                        end_time=time.time()
                        process_time=end_time-start_time
                        start_time=end_time
                        #左腳腳跟 y z
                        left_y_value_list.append(line_left_heel[1])
                        left_depth_value_mediapipe_calibrate_list.append(depth_value_mediapipe_calibrate_left_heel) 
                        ##右腳腳跟 y z
                        right_y_value_list.append(line_right_heel[1])
                        right_depth_value_mediapipe_calibrate_list.append(depth_value_mediapipe_calibrate_right_heel)
                        
                        foot_step_time.append(process_time)
                        
                        #y depth heel 
                        #x degree toe
                        left_x_value_list.append(line_left_knee[1])
                        left_line_degree.append(depth_value_mediapipe_calibrate_left_knee) 
                        
                        right_x_value_list.append(line_right_knee[1])
                        right_line_degree.append(depth_value_mediapipe_calibrate_right_knee)
                        #self.show_foot_step(self.left_y_value_list,self.left_depth_value_mediapipe_calibrate_list,self.right_y_value_list,self.right_depth_value_mediapipe_calibrate_list)
                        show_foot_step_distance(left_depth_value_mediapipe_calibrate_list,right_depth_value_mediapipe_calibrate_list)
       


                    #23 24 髖關節   
                    #25 26 膝關節
# 绘制关键点连线
            print(results.pose_landmarks.landmark[0])
            #draw_custom_landmarks(color_image, results.pose_landmarks, selected_points, custom_connections)
            mp_drawing.draw_landmarks(color_image, results.pose_landmarks, connections=custom_connections)
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        out.write(color_image)
        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        
        if cv2.waitKey(5) == ord('q'):
            break     # 按下 q 鍵停止

finally:

    # Stop streaming
    np.save("degree.npy",line_degree)
    np.save("x.npy",x_value_list)
    np.save("y.npy",y_value_list)
    np.save("depth.npy",depth_value_mediapipe_calibrate_list)
    out.release()
    pipeline.stop()
