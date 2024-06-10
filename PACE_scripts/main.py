#!source /storage/home/hcoda1/3/ydhadwal3/myenv/bin/activate

import deeplabcut

yaml_path = "/storage/home/hcoda1/3/ydhadwal3/p-fnajafi3-0/FN16-PupilTrace-YD-2024-05-29/config.yaml"
video_path = "/storage/coda1/p-fnajafi3/0/ydhadwal3/FN16-Pupil-Source-Videos_15-21"
output_folder = "/storage/home/hcoda1/3/ydhadwal3/p-fnajafi3-0/FN16-PupilTrace-YD-2024-05-29/output"

#deeplabcut.create_training_dataset(yaml_path, augmenter_type='imgaug')

#deeplabcut.train_network(yaml_path, maxiters=200000, saveiters=50000, max_snapshots_to_keep=3)

#deeplabcut.evaluate_network(yaml_path, plotting=True)

deeplabcut.analyze_videos(yaml_path, [video_path], videotype='avi', destfolder=output_folder, save_as_csv=True)