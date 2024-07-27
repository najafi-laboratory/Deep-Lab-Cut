import numpy as np
import h5py
import pandas as pd
import cv2

video = "FN16_P_20240621_js_t_cam0_run002_20240621_152415.avi"

def read_raw_voltages():
    f = h5py.File(
        'raw_voltages.h5',
        'r')
    vol_time = np.array(f['raw']['vol_time'])
    vol_start_bin = np.array(f['raw']['vol_start_bin'])
    vol_stim_bin = np.array(f['raw']['vol_stim_bin'])
    vol_img_bin = np.array(f['raw']['vol_img_bin'])
    f.close()
    return [vol_time, vol_start_bin, vol_stim_bin, vol_img_bin]


voltage = read_raw_voltages()
# print(voltage)
voltage_df = pd.DataFrame(columns=["time", "vol_img_bin"])
voltage_df["time"] = voltage[0]
voltage_df["vol_img_bin"] = voltage[3]

voltage_csv = pd.DataFrame(columns=["vol_time", "vol_start_bin", "vol_stim_bin", "vol_img_bin"])
voltage_csv["vol_time"] = voltage[0]
voltage_csv["vol_start_bin"] = voltage[1]
voltage_csv["vol_stim_bin"] = voltage[2]
voltage_csv["vol_img_bin"] = voltage[3]
voltage_csv.to_csv('voltage.csv')

camlog = pd.read_excel("camlog.xlsx")

cap = cv2.VideoCapture(video)

fps = cap.get(cv2.CAP_PROP_FPS)
frame_duration_ms = 1000 / fps

ms_per_frame_voltage = []
ms_per_frame_camlog = []
ms_per_frame_cv2 = []
ms_per_frame = pd.DataFrame(columns=["voltage", "camlog", "cv2"])

for index, row in voltage_df.iterrows():
    if index == 0:
        continue
    if len(ms_per_frame_voltage) == len(camlog):
        break
    if row["vol_img_bin"] != 1.0 and len(ms_per_frame_voltage) == 0:
        ms_per_frame_voltage.append(row["time"])
    if row["vol_img_bin"] != 1.0 and row["time"] - ms_per_frame_voltage[-1] > 2:
        ms_per_frame_voltage.append(row["time"])


for index, row in camlog.iterrows():
    if index == 0:
        continue
        # Needed to keep dataframe rows aligned (camlog collects data for 4 more rows which are ignored this way)
    if len(ms_per_frame_camlog) == len(ms_per_frame_voltage):
        break
    time = row["Time"] - camlog.iloc[0, 0]
    ms_per_frame_camlog.append(time * 1000)
    ms_per_frame_cv2.append(frame_duration_ms * index)

ms_per_frame["voltage"] = ms_per_frame_voltage[0: len(ms_per_frame_camlog)]
ms_per_frame["camlog"] = ms_per_frame_camlog
ms_per_frame["cv2"] = ms_per_frame_cv2

ms_per_frame.to_excel("voltage_camlog_frames_aligned.xlsx")
