import deeplabcut

yaml_path = "/storage/coda1/p-fnajafi3/0/ydhadwal3/20240710-Yuvraj_Dhadwal-2024-07-24/config.yaml"
video_path = "/storage/coda1/p-fnajafi3/0/ydhadwal3/20240710-Yuvraj_Dhadwal-2024-07-24/videos"
output_folder = "/storage/coda1/p-fnajafi3/0/ydhadwal3/20240710-Yuvraj_Dhadwal-2024-07-24/output"

# deeplabcut.create_training_dataset(yaml_path, augmenter_type='imgaug')

deeplabcut.train_network(yaml_path, maxiters=200000, saveiters=50000, max_snapshots_to_keep=3)

# deeplabcut.evaluate_network(yaml_path, plotting=True)

# deeplabcut.analyze_videos(yaml_path, [video_path], videotype='avi', destfolder=output_folder, save_as_csv=True)