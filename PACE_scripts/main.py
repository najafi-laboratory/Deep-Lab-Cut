#!source /storage/home/hcoda1/3/ydhadwal3/myenv/bin/activate

import deeplabcut

yaml_path = "/storage/coda1/p-fnajafi3/0/ydhadwal3/FN13_Joystick_0603-Yuvraj-2024-06-17/config.yaml"
video_path = "/storage/coda1/p-fnajafi3/0/shared/2P_Imaging/video_data/FN16_P_20240603_js_t_cam0_run003_20240603_100906.avi"
output_folder = "/storage/coda1/p-fnajafi3/0/ydhadwal3/FN13_Joystick_0603-Yuvraj-2024-06-17/output"

deeplabcut.create_training_dataset(yaml_path, augmenter_type='imgaug')

deeplabcut.train_network(yaml_path, maxiters=350000, saveiters=50000, max_snapshots_to_keep=3)

#deeplabcut.evaluate_network(yaml_path, plotting=True)

#deeplabcut.analyze_videos(yaml_path, [video_path], videotype='avi', destfolder=output_folder, save_as_csv=True)