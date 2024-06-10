import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def find_smallest_positive(num1, num2, num3):
    # Create a list of the numbers
    numbers = [num1, num2, num3]

    # Filter to include only positive numbers
    positive_numbers = [num for num in numbers if num > 0]

    # Find the smallest positive number or set to 0 if there are none
    if positive_numbers:
        smallest_positive = min(positive_numbers)
    else:
        smallest_positive = 0

    return smallest_positive


def largest_valid_index(indexes, lst):
    # Length of the list
    length = len(lst)

    # Filter indexes to include only those smaller than the length of the list
    valid_indexes = [idx for idx in indexes if idx < length]

    # Find the largest valid index or return None if there are no valid indexes
    if valid_indexes:
        largest_index = max(valid_indexes)
    else:
        largest_index = indexes[0] - 1

    return largest_index


voltage = pd.read_csv("../2p_camlog_alignment/voltage.csv")

voltage_stim = []

last_stim = 0

for index, row in voltage.iterrows():
    if row["vol_stim"] == 1 and row["vol_stim"] != last_stim:
        voltage_stim.append(row["time"])
        last_stim = 1
    elif row["vol_stim"] != last_stim:
        last_stim = 0

frame_times = pd.read_excel("voltage_camlog_frames_aligned.xlsx").iloc[:, 2]
avg = pd.read_csv("area_per_frame.csv")
y = []
for index, row in avg.iterrows():
    if row[1] > 1750 or row[1] < 600:
        y.append(0.33 * y[-3] + 0.33 * y[-2] + 0.33 * y[-1])
    else:
        y.append(row[1])
area_per_frame = pd.DataFrame()
area_per_frame['area'] = y

j = 0

pupil_area_per_stim = []
pupil_stim_frames = []

for i in range(len(frame_times)):
    if j >= len(voltage_stim):
        break
    if frame_times.get(i) > voltage_stim[j]:
        if abs(frame_times.get(i) - voltage_stim[j] + 16) > abs(frame_times.get(i-1) - voltage_stim[j] + 16):
            pupil_area_per_stim.append(area_per_frame.iloc[i - 64 : i + 65, 0])
            pupil_stim_frames.append(i)
        else:
            pupil_area_per_stim.append(area_per_frame.iloc[i - 65 : i + 64, 0])
            pupil_stim_frames.append(i-1)
        j = j + 1

index = 0

while index < 300:
    fig = make_subplots(rows=int(len(pupil_area_per_stim) / 300), cols=1)

    for i in range(index*int(len(pupil_area_per_stim)/300), (index+1)*int(len(pupil_area_per_stim)/300)):
        fig.append_trace(go.Scatter(
            x=pupil_area_per_stim[i].index,
            y=list(pupil_area_per_stim[i]),
            showlegend=False,
            line=dict(color='black'),
        ), row=i + 1 - index*int(len(pupil_area_per_stim)/300), col=1)

        start = find_smallest_positive(i - 3, i - 2, i - 1)
        end = largest_valid_index([i + 1, i + 2, i + 3], pupil_stim_frames)

        j = 0
        y = []

        while start <= end and j < len(pupil_area_per_stim[i]):
            if pupil_area_per_stim[i].index[j] < pupil_stim_frames[start]:
                y.append(1000)
                j = j + 1
            else:
                j = j + 6
                start = start + 1
                for z in range(6):
                    y.append(1200)

        if end == len(pupil_stim_frames) - 1:
            for z in range(len(y), len(pupil_area_per_stim[i])):
                y.append(1000)

        fig.append_trace(go.Scatter(
            x=pupil_area_per_stim[i].index,
            y=y,
            showlegend=False,
            line=dict(color='green'),
        ), row=i + 1 - index*int(len(pupil_area_per_stim)/300), col=1)

        fig.update_layout(title=str(index + 1) + " Pupil Area vs Voltage Stim", height=1000, width=1250, plot_bgcolor="white")

        fig.update_xaxes(row=i + 1 - index*int(len(pupil_area_per_stim)/300), col=1, title_text="Time (Seconds)", showline=True, linewidth=2, linecolor='black',
                         tickvals=list(range(pupil_stim_frames[i], pupil_area_per_stim[i].index[0], -15)) + (
                             list(range(pupil_stim_frames[i], pupil_area_per_stim[i].index[-1], 15))),
                         ticktext=[0, -0.5, -1, -1.5, -2, 0.5, 0.5, 1, 1.5, 2], ticks="outside", tickwidth=1,
                         tickcolor='black', ticklen=7)
        fig.update_yaxes(row=i + 1 - index*int(len(pupil_area_per_stim)/300), col=1, title_text="Area (Pixels)", showline=True, linewidth=2, linecolor='black',
                         dtick=100,
                         tickvals=list(range(800, 1601, 100)),
                         ticktext=[800, " ", 1000, " ", 1200, " ", 1400, " ", 1600],
                         ticks="outside", tickwidth=1, tickcolor='black', ticklen=7)

    if index < 5:
        fig.show()
    fig.write_html(str(index + 1) + "_pupil_area_vs_voltage_stim.html")
    index = index + 1




