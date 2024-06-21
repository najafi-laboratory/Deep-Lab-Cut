To start data analysis, there are a few key steps.

1. First you must build a Deep Learning model to trace the perimeter of mouse pupil using 12 points.
2. Using your deep learning model, analyze the video and track the pixel locations of the 12 points.
3. Once you have this data ready, you must feed this into Pupil-Area-Calculations.py \
    a. This file will calculate the area of the pupil for each frame based on the trace data inputted.
4. Input this new csv file into Pupil-Area-Graphing.py \
    a. This file will ensure there are no outliers in your data and will output this clean data as well as save and share a graphical representation of Pupil Area vs. Frames.
5. Download the camlog, raw_voltages.h5, and video files \
    a. Create an excel file of the camlog where the first row is labelled "Time" and the rest of the rows are the timestamps
6. 
