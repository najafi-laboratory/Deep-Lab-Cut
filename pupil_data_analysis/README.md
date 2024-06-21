To start data analysis, there are a few key steps.

1. First you must build a Deep Learning model to trace the perimeter of mouse pupil using 12 points.
2. Using your deep learning model, analyze the video and track the pixel locations of the 12 points.
3. Once you have this data ready, you must feed this into Pupil-Area-Calculations.py \
    a. This file will calculate the area of the pupil for each frame based on the trace data inputted.
4. Input this new csv file into Pupil-Area-Graphing.py \
    a. This file will ensure there are no outliers in your data and will output this clean data as well as save and share a graphical representation of Pupil Area vs. Frames.
5. Download the camlog, raw_voltages.h5, and video files \
    a. Create an excel file of the camlog where the first row is labelled "Time" and the rest of the rows are the timestamps
6. Using these three files, run Voltage-Reader.py \
    a. This file will calculate the timestamps for each new frame based on that of the camera, 2p-imaging rig, and generic 30 fps and output an excel file \
    b. This file will also create another csv: voltage.csv
7. Now it is time to run onset_time_alignment.py \
    a. This file will take the voltage csv file and calculate all the times when a stimulus is shown to a mouse
    b. Then for each stimulus, it will save a list of all the frames 2 seconds before and 2 seconds after
    c. Then it will graph each of these where pupil area and stimuli are graphed on same plane to see relationship. There will be 100 graphs in each graph set.
    d. It will save all these graph sets and show a few of them.
    e. Afterwards it will calculate the average area of the pupil for each frame in the 4 second intervals for each stimulus
    f. It will show and save this graph and one where pupil area is standardized.
