import os
import json
import h5py
import shutil
import argparse
import numpy as np
import pandas as pd
from datetime import datetime

def process_vol():

    # read the voltage recording file.
    def read_vol_to_np():
        # voltage: SESSION_Cycle00001_VoltageRecording_000NUM.csv.
        df_vol = pd.read_csv(
            "../Mice Voltages/FN16-20240621/FN16_P_20240621_js_t-047_Cycle00001_VoltageRecording_001.csv",
            engine='python')


        # time index in ms.
        vol_time  = df_vol['Time(ms)'].to_numpy()
        # AI0: Bpod BNC1 (trial start signal from bpod).
        if ' Input 0' in df_vol.columns.tolist():
            vol_start = df_vol[' Input 0'].to_numpy()
        else:
            vol_start = np.zeros_like(vol_time)
        # AI1: sync patch and photodiode (visual stimulus).
        if ' Input 1' in df_vol.columns.tolist():
            vol_stim_vis = df_vol[' Input 1'].to_numpy()
        else:
            vol_stim_vis = np.zeros_like(vol_time)
        # AI2: HIFI BNC output.
        if ' Input 2' in df_vol.columns.tolist():
            vol_hifi = df_vol[' Input 2'].to_numpy()
        else:
            vol_hifi = np.zeros_like(vol_time)
        # AI3: ETL scope imaging output (2p microscope image trigger signal).
        if ' Input 3' in df_vol.columns.tolist():
            vol_img = df_vol[' Input 3'].to_numpy()
        else:
            vol_img = np.zeros_like(vol_time)
        # AI4: Hifi audio output waveform (HIFI waveform signal).
        if ' Input 4' in df_vol.columns.tolist():
            vol_stim_aud = df_vol[' Input 4'].to_numpy()
        else:
            vol_stim_aud = np.zeros_like(vol_time)
        # AI5: FLIR output.
        if ' Input 5' in df_vol.columns.tolist():
            vol_flir = df_vol[' Input 5'].to_numpy()
        else:
            vol_flir = np.zeros_like(vol_time)
        # AI6: PMT shutter.
        if ' Input 6' in df_vol.columns.tolist():
            vol_pmt = df_vol[' Input 6'].to_numpy()
        else:
            vol_pmt = np.zeros_like(vol_time)
        # AI7: PMT shutter.
        if ' Input 7' in df_vol.columns.tolist():
            vol_led = df_vol[' Input 7'].to_numpy()
        else:
            vol_led = np.zeros_like(vol_time)
        vol = {
            'vol_time'     : vol_time,
            'vol_start'    : vol_start,
            'vol_stim_vis' : vol_stim_vis,
            'vol_hifi'     : vol_hifi,
            'vol_img'      : vol_img,
            'vol_stim_aud' : vol_stim_aud,
            'vol_flir'     : vol_flir,
            'vol_pmt'      : vol_pmt,
            'vol_led'      : vol_led
            }
        return vol

    # threshold the continuous voltage recordings to 01 series.
    def thres_binary(
            data,
            thres
            ):
        data_bin = data.copy()
        data_bin[data_bin<thres] = 0
        data_bin[data_bin>thres] = 1
        return data_bin

    # convert all voltage recordings to binary series.
    def vol_to_binary(vol):
        vol['vol_start']    = thres_binary(vol['vol_start'],    1)
        vol['vol_stim_vis'] = thres_binary(vol['vol_stim_vis'], 1)
        vol['vol_hifi']     = thres_binary(vol['vol_hifi'],     0.5)
        vol['vol_img']      = thres_binary(vol['vol_img'],      1)
        vol['vol_flir']     = thres_binary(vol['vol_flir'],     0.5)
        return vol

    # save voltage data.
    def save_vol(vol):
        # file structure:
        # args.save_path / raw_voltages.h5
        # -- raw
        # ---- vol_time
        # ---- vol_start_bin
        # ---- vol_stim_bin
        # ---- vol_img_bin
        f = h5py.File('raw_voltages.h5', 'w')
        grp = f.create_group('raw')
        grp['vol_time']      = vol['vol_time']
        grp['vol_start_bin'] = vol['vol_start']
        grp['vol_stim_bin']  = vol['vol_stim_vis']
        grp['vol_hifi']      = vol['vol_hifi']
        grp['vol_img_bin']   = vol['vol_img']
        grp['vol_stim_aud']  = vol['vol_stim_aud']
        grp['vol_flir']      = vol['vol_flir']
        grp['vol_pmt']       = vol['vol_pmt']
        f.close()

    # run processing.
    try:
        print('run')
        vol = read_vol_to_np()
        print('1')
        vol = vol_to_binary(vol)
        print('2')
        save_vol(vol)
        print('3')
    except:
        print('Valid voltage recordings csv file not found')

if __name__ == "__main__":

    process_vol()