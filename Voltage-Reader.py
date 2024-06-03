import numpy as np
import h5py
import pandas as pd

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
df = pd.DataFrame(columns=["time", "vol_stim"])
df["time"] = voltage[0]
df["vol_stim"] = voltage[1]
#
df.to_csv("voltage.csv")