import pandas as pd
import numpy as np
import os
os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
import h5py
import dask
from dask import delayed
from dask.distributed import Client, LocalCluster
import gc


@delayed
def process_vol(file_path, session_name):
    
    def preprocess(df):
        # time index in ms.
        vol_time = df['Time(ms)'].to_numpy()
        # AI0: Bpod BNC1 (trial start signal from bpod).
        if ' Input 0' in df.columns:
            vol_start = df[' Input 0'].to_numpy()
        else:
            vol_start = np.zeros_like(vol_time).astype(np.float32)
        
        # AI1: sync patch and photodiode (visual stimulus).
        if ' Input 1' in df.columns:
            vol_stim_vis = df[' Input 1'].to_numpy()
        else:
            vol_stim_vis = np.zeros_like(vol_time).astype(np.float32)
            
         # AI2: HIFI BNC output.
        if  ' Input 2' in df.columns:
            vol_hifi = df[' Input 2'].to_numpy()
        else:
            vol_hifi = np.zeros_like(vol_time).astype(np.float32)
            
        # AI3: ETL scope imaging output (2p microscope image trigger signal).
        if ' Input 3' in df.columns:
            vol_img = df[' Input 3'].to_numpy()
        else:
            vol_img = np.zeros_like(vol_time).astype(np.float32)
            
        # AI4: Hifi audio output waveform (HIFI waveform signal).
        if ' Input 4' in df.columns:
            vol_stim_aud = df[' Input 4'].to_numpy()
        else:
            vol_stim_aud = np.zeros_like(vol_time).astype(np.float32)
            
        # AI5: FLIR output.
        if ' Input 5' in df.columns:
            vol_flir = df[' Input 5'].to_numpy()
        else:
            vol_flir = np.zeros_like(vol_time).astype(np.float32)
            
        # AI6: PMT shutter.
        if ' Input 6' in df.columns:
            vol_pmt = df[' Input 6'].to_numpy()
        else:
            vol_pmt = np.zeros_like(vol_time).astype(np.float32)
            
        # AI7: PMT shutter.
        if ' Input 7' in df.columns:
            vol_led = df[' Input 7'].to_numpy()
        else:
            vol_led = np.zeros_like(vol_time).astype(np.float32)
            
        return pd.DataFrame({
            'vol_time'     : vol_time,
            'vol_start'    : vol_start,
            'vol_stim_vis' : vol_stim_vis,
            'vol_hifi'     : vol_hifi,
            'vol_img'      : vol_img,
            'vol_stim_aud' : vol_stim_aud,
            'vol_flir'     : vol_flir,
            'vol_pmt'      : vol_pmt,
            'vol_led'      : vol_led
        })
        
        
    def thres_binary(data, thres):
        return (data > thres).astype('uint8')
        
    def df_to_binary(df):
        df['vol_start'] = thres_binary(df['vol_start'], 1)
        df['vol_stim_vis'] = thres_binary(df['vol_stim_vis'], 1)
        df['vol_hifi'] = thres_binary(df['vol_hifi'], 0.5)
        df['vol_img'] = thres_binary(df['vol_img'], 1)
        df['vol_flir'] = thres_binary(df['vol_flir'], 0.5)
        
        return df
    
    if file_path.endswith('csv') or file_path.endswith('h5'):
        
        print(f'Start to process {session_name}')
        if file_path.endswith('csv'):
            vol_folder = os.path.dirname(file_path)
            #target_cols = ['Time(ms)', ' Input 0', ' Input 1', ' Input 2', ' Input 3', ' Input 4', ' Input 5', ' Input 6', ' Input 7']
            
            with h5py.File(f'{vol_folder}/raw_voltage/{session_name}_raw_voltages.h5', 'w') as f:
                grp = f.create_group('raw')
                
                df = pd.read_csv(file_path, engine='c', dtype=np.float32)
                df = preprocess(df)
                df = df_to_binary(df)
                
                for col in df.columns:
                    grp.create_dataset(col, data=df[col], dtype=df[col].dtype)
        print(f'Process {session_name} ends!')

def get_trigger_time(vol_time, vol_bin):
    diff_vol = np.diff(vol_bin, prepend=0)
    idx_up = np.where(diff_vol == 1)[0]
    idx_down = np.where(diff_vol == -1)[0]
    time_up = vol_time[idx_up]
    time_down = vol_time[idx_down]
    return time_up, time_down

def correct_time_img_center(time_img):
    # find the frame internal.
    diff_time_img = np.diff(time_img, append=0)
    # correct the last element.
    diff_time_img[-1] = np.mean(diff_time_img[:-1])
    # move the image timing to the center of photon integration interval.
    diff_time_img = diff_time_img / 2
    # correct each individual timing.
    time_img = time_img + diff_time_img
    return time_img


def process(file_path, downsampling=1,): 
    with h5py.File(file_path, 'r', libver='latest', swmr=True) as f:  # Use SWMR for better performance
        vol_time = f['raw']['vol_time'][::downsampling]
        vol_img = f['raw']['vol_img'][::downsampling]
    
    time_up, time_down = get_trigger_time(vol_time, vol_img)
    return time_up, time_down


def get_image_time(raw_vol_directory):  # Reduced chunk size
    image_time = 0
    if raw_vol_directory.endswith('.h5') and '_raw_' in raw_vol_directory:
        time_up, time_down = process(raw_vol_directory, downsampling=1)
        image_time = correct_time_img_center(time_up)
        
        del time_up, time_down
        gc.collect()
        
    return len(image_time)
    
def read_and_preprocessing_camlog(camlog_path):
    camlog = []
    with open(camlog_path, 'r') as f:
        for line in f:
            if not line.startswith('#'):
                camlog.append(line.split(',')[1])
    return np.array(camlog, dtype=np.float32)
    
def write_temp_final_result(camlog, pupil_area, root_path, session_name, qualified=True):
    path = f'{root_path}/result/camera_dlc/camera_{session_name}.h5' if qualified else f'{root_path}/result/camera_dlc/under_qualified/camera_{session_name}.h5'
    
    with h5py.File(path, 'w') as f:
        grp = f.create_group('camera_dlc')
        grp.create_dataset('camera_time', data=camlog)
        grp.create_dataset('pupil', data=pupil_area)
    
                
# Define a function to calculate the area using the Shoelace formula
def shoelace_formula(x, y):
    # Ensure the polygon is closed by appending the first point to the end
    
    x = np.concatenate([x, x[:, [0]]], axis=1)
    y = np.concatenate([y, y[:, [0]]], axis=1)

    # Apply Shoelace formula
    area = 0.5 * abs(np.sum(x[:, :-1] * y[:, 1:] - y[:, :-1] * x[:, 1:], axis=1))
    return area
    
    
@delayed
def calculate_area(pupil_data_path, raw_vol_directory, camlog_file_path, session_name, truncate=True, emergency=False):

    # Processing final res
    print(f'Getting the camlog for {session_name} start!')
    camlog = read_and_preprocessing_camlog(camlog_file_path)
    print(f'Getting the camlog for {session_name} end!')

    print(f'Getting the correct time stampts for {session_name} start!')
    correct_time_stamps = get_image_time(raw_vol_directory) if not emergency else len(camlog)
    print(f'Getting the correct time stampts for {session_name} end!')
    
    print(f'Calculating the area for {session_name} start!')
    # Read the file
    data = pd.read_csv(pupil_data_path, nrows=2)
    data = data.drop(columns=['scorer'])

    # Get the coordinates
    coordinate_cols_x = data.columns[0::3]
    coordinate_cols_y = data.columns[1::3]

    center_x_col = data.columns[72]
    center_y_col = data.columns[73]

    pupil_cols_x = coordinate_cols_x[:12]
    eye_cols_x = coordinate_cols_x[12:24]

    pupil_cols_y = coordinate_cols_y[:12]
    eye_cols_y = coordinate_cols_y[12:24]
    
    #############
    # Clean data
    del data
    gc.collect()
    #############
    
    df = pd.read_csv(pupil_data_path,
                             skiprows=[1, 2],
                             usecols=list(pupil_cols_x) + list(pupil_cols_y) + list(eye_cols_x) + list(eye_cols_y) + [center_x_col] + [center_y_col],
                             dtype=np.float32)
        
    pupil_coords_x = df.loc[:, pupil_cols_x].values
    pupil_coords_y = df.loc[:, pupil_cols_y].values
    center_x = df.loc[:, center_x_col].values
    pupil_area = shoelace_formula(pupil_coords_x, pupil_coords_y)
    
    eye_coords_x = df.loc[:, eye_cols_x].values
    eye_coords_y = df.loc[:, eye_cols_y].values
    center_y = df.loc[:, center_y_col].values
    eye_area = shoelace_formula(eye_coords_x, eye_coords_y)
    
    
    if truncate:
        if len(pupil_area) >= correct_time_stamps:
            pupil_area = pupil_area[:correct_time_stamps]
            area = pd.DataFrame({
                'Pupil_Area' : pupil_area,
                'Eye_Area' : eye_area[:correct_time_stamps],
                'Center_X' : center_x[:correct_time_stamps],
                'Center_Y' : center_y[:correct_time_stamps]
            })

            pupil_data_folder_path = os.path.dirname(pupil_data_path)
            write_temp_final_result(camlog, pupil_area, pupil_data_folder_path, session_name)
            area.to_csv(f'{pupil_data_folder_path}/result/area/{session_name}_area.csv', index=False)
            print(f'Calculating the area for {session_name} end!')
        else:
            area = pd.DataFrame({
                'Pupil_Area' : pupil_area,
                'Eye_Area' : eye_area,
                'Center_X' : center_x,
                'Center_Y' : center_y
            })
        
            pupil_data_folder_path = os.path.dirname(pupil_data_path)
            write_temp_final_result(camlog, pupil_area, pupil_data_folder_path, session_name, qualified=False)
            area.to_csv(f'{pupil_data_folder_path}/result/area/under_qualified/under_qualified_{session_name}_area.csv', index=False)
            print(f'Calculating the area for {session_name} end!')
    else:
        area = pd.DataFrame({
                'Pupil_Area' : pupil_area,
                'Eye_Area' : eye_area,
                'Center_X' : center_x,
                'Center_Y' : center_y
            })
        pupil_data_folder_path = os.path.dirname(pupil_data_path)
        area.to_csv(f'{pupil_data_folder_path}/result/area/no_truncate/{session_name}_area.csv', index=False)
        print(f'Calculating the area no truncate for {session_name} end!')


if __name__ == '__main__':

    dask.config.set({
        "distributed.worker.heartbeat.interval" : "10s",
        "distributed.worker.heartbeat.timeout" : '120s',
        "distributed.comm.timeouts.tcp" : "120s",
        "distributed.scheduler.worker-ttl" : "120s",
        "distributed.worker.memory.target" : 0.7,
        "distributed.worker.memory.spill" : 0.9
    })
    
    emergency = False
    truncate = True
    
    vol_recording = '/storage/project/r-fnajafi3-0/yyu496/vol/Voltage_Recording'
    pupil_coords = '/storage/project/r-fnajafi3-0/yyu496/pupile_preprocessing/Yicong_method/pupil_coords'
    raw_vol = '/storage/project/r-fnajafi3-0/yyu496/vol/Voltage_Recording/raw_voltage'
    camlog_path = '/storage/project/r-fnajafi3-0/yyu496/pupile_preprocessing/Yicong_method/camlog'


    cluster = LocalCluster(n_workers=12,
                           threads_per_worker=1,
                           memory_limit='16GB')
    
    with Client(cluster) as c:
    
        vol_tasks = []
        for vol_file in [f for f in os.listdir(vol_recording) if f.endswith('.csv')]:
            vol_path = os.path.join(vol_recording, vol_file)
            session_name = vol_file.split('-')[0]
            vol_tasks.append(process_vol(vol_path, session_name))
        dask.compute(*vol_tasks)
        
        area_calculation_tasks = []
        
        if not emergency:
            for pupil_coords_file, raw_vol_file, camlog_file in zip(
                sorted([area for area in os.listdir(pupil_coords) if area.endswith('.csv')]),
                sorted([vol for vol in os.listdir(raw_vol) if vol.endswith('.h5') and '_raw_' in vol]),
                sorted([camlog for camlog in os.listdir(camlog_path)])):
                
                session_name = pupil_coords_file.split('_cropped')[0]
                pupil_coords_path = os.path.join(pupil_coords, pupil_coords_file)
                raw_vol_path = os.path.join(raw_vol, raw_vol_file)
                camlog_file_path = os.path.join(camlog_path, camlog_file)
                
                area_calculation_tasks.append(calculate_area(pupil_coords_path, raw_vol_path, camlog_file_path, session_name, truncate=truncate))
            dask.compute(*area_calculation_tasks)
        else:
            for pupil_coords_file, camlog_file in zip(
                sorted([area for area in os.listdir(pupil_coords) if area.endswith('.csv')]),
                sorted([camlog for camlog in os.listdir(camlog_path)])):
                
                session_name = pupil_coords_file.split('_cropped')[0]
                pupil_coords_path = os.path.join(pupil_coords, pupil_coords_file)
                raw_vol_path = None
                camlog_file_path = os.path.join(camlog_path, camlog_file)
                
                area_calculation_tasks.append(calculate_area(pupil_coords_path, raw_vol_path, camlog_file_path, session_name, truncate=truncate, emergency=emergency))
            dask.compute(*area_calculation_tasks)