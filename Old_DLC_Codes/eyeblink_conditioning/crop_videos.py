import cv2
import os

input_folder = 'input_videos'
output_folder = 'output_videos'

# creates directory to saved cropped videos to
os.makedirs(output_folder, exist_ok=True)
x, y, width, height = 230, 80, 100, 100

def crop_videos(input_path, output_path, x, y, width, height):
    # Create Video Object
    cap = cv2.VideoCapture(input_path)

    # Get original video details
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Create the cropped video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Crop frame
        cropped_frame = frame[y:y+height, x:x+width]
        out.write(cropped_frame)

    cap.release()
    out.release()

for file in os.listdir(input_folder):
    if file.endswith('.avi'):
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f'cropped_{file}')

        crop_videos(input_path, output_path, x, y, width, height)
        print(f'Processed {file} -> {output_path}')

print("All videos cropped!")
