import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sklearn.preprocessing import StandardScaler
import math
import plotly.io as pio


def find_smallest_positive(i, startingIndex, stim_frames):
    # Create a list of the numbers
    numbers = [i - 5, i - 4, i - 3, i - 2, i - 1, i]

    # Filter to include only positive numbers
    positive_numbers = [num for num in numbers if num > 0]
    smallest_positive = 0

    # Find the smallest positive number or set to 0 if there are none
    while True:
        if positive_numbers:
            smallest_positive = min(positive_numbers)
        else:
            smallest_positive = 0

        if stim_frames[smallest_positive] < startingIndex:
            positive_numbers.remove(smallest_positive)
        else:
            break

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


# Take User Input on Mouse Name
# mouse = input("What is the Mouse Name and Session ID? (EX: VG01_20240515)       ")
mouse = "FN16_20240621"

# Convert relevant csv/excel files into Pandas Data Frames
frame_times = pd.read_excel("voltage_camlog_frames_aligned.xlsx").iloc[:, 2]
voltage_times = pd.read_excel("voltage_camlog_frames_aligned.xlsx").iloc[:, 1]
voltage = pd.read_csv("voltage.csv")
area_per_frame = pd.read_csv("area_per_frame_no_outliers.csv")

# Voltage stim is a list containing times when 2p imaging voltage first spikes
voltage_stim = []
last_stim = 0

# Calculates whenever voltage stim turns on and saves to list
for index, row in voltage.iterrows():
    if row["vol_stim_bin"] == 1 and row["vol_stim_bin"] != last_stim:
        voltage_stim.append(row["vol_time"])
        last_stim = 1
    elif row["vol_stim_bin"] != last_stim:
        last_stim = 0

j = 0

# List of Pandas Series where index is index of 2p voltage spike and
# Series is pupil area 2 seconds before and after the spike
pupil_area_per_stim = []
# List of frames associated with 2p voltage spikes
pupil_stim_frames = []
# List of Pandas Series where index is index of 2p voltage spike and
# Series is stim value 2 seconds before and after the spike
stims = []

# # saves all the pupil data 2 seconds before and 2 seconds after stim onset time
for i in range(len(frame_times)):
    if j >= len(voltage_stim):
        break
    if frame_times.get(i) > voltage_stim[j]:
        if abs(frame_times.get(i) - voltage_stim[j] + 16) > abs(frame_times.get(i - 1) - voltage_stim[j] + 16):
            pupil_area_per_stim.append(area_per_frame.iloc[i - 64: i + 65, 1])
            stims.append(voltage.iloc[int(voltage_times[i] * 2) - 2000: int(voltage_times[i] * 2) + 2030, 3])
            pupil_stim_frames.append(i)
        else:
            pupil_area_per_stim.append(area_per_frame.iloc[i - 65: i + 64, 1])
            pupil_stim_frames.append(i - 1)
            stims.append(voltage.iloc[int(voltage_times[i] * 2) - 2030: int(voltage_times[i] * 2) + 2000, 3])
        j = j + 1

# Creates a Graph Set of Subplots where each Graph Set contains ~100 Subplots graphing pupil area vs stim values
index = 0
maxIndex = int(len(pupil_area_per_stim) / 100)

while index < maxIndex:
    # Creates each subplot and creates a placeholder subplot title
    fig = make_subplots(rows=int(len(pupil_area_per_stim) / maxIndex), cols=1, subplot_titles=['temp_subtitle'
                                                                                               for date in np.arange(
                                                                                                len(pupil_area_per_stim)
                                                                                                )])
    # Creates pupil area subplot graphs in each graphset
    for i in range(index * int(len(pupil_area_per_stim) / maxIndex),
                   (index + 1) * int(len(pupil_area_per_stim) / maxIndex)):
        fig.append_trace(go.Scatter(
            x=pupil_area_per_stim[i].index,
            y=list(pupil_area_per_stim[i]),
            showlegend=False,
            line=dict(color='black'),
        ), row=i + 1 - index * int(len(pupil_area_per_stim) / maxIndex), col=1)

        j = 0
        y = []
        # Finds number of stim spikes before and after current stim spike that are in each subplot
        start = find_smallest_positive(i, pupil_area_per_stim[i].index[0], pupil_stim_frames)
        end = largest_valid_index([i + 1, i + 2, i + 3], pupil_stim_frames)

        # Manually graphs stim values since pupil area is calculated per frame but stims are calculated as 1/2 ms
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

        # Adds the stim trace onto the subplots
        fig.append_trace(go.Scatter(
            x=pupil_area_per_stim[i].index,
            y=y,
            showlegend=False,
            line=dict(color='green'),
        ), row=i + 1 - index * int(len(pupil_area_per_stim) / maxIndex), col=1)

        # Updates all the labels around each of the subplots
        fig.layout.annotations[i - index * int(len(pupil_area_per_stim) / maxIndex)]['text'] = "Subplot " + str(
            i + 1) + ": Frames " + str(pupil_area_per_stim[i].index[0]) + " - " + str(
            pupil_area_per_stim[i].index[-1]) + " and Seconds: " + str(
            round(pupil_area_per_stim[i].index[0] / 30)) + " - " + str(round(pupil_area_per_stim[i].index[-1] / 30))
        fig.update_xaxes(row=i + 1 - index * int(len(pupil_area_per_stim) / maxIndex),
                         col=1,
                         title_text="Time (Seconds)",
                         showline=True,
                         linewidth=2,
                         linecolor='black',
                         tickvals=list(range(pupil_stim_frames[i], pupil_area_per_stim[i].index[0], -15)) + (
                             list(range(pupil_stim_frames[i], pupil_area_per_stim[i].index[-1], 15))),
                         ticktext=[0, -0.5, -1, -1.5, -2, 0.5, 0.5, 1, 1.5, 2],
                         ticks="outside",
                         tickwidth=1,
                         tickcolor='black',
                         ticklen=7)
        fig.update_yaxes(row=i + 1 - index * int(len(pupil_area_per_stim) / maxIndex),
                         col=1,
                         title_text="Pupil Area (Pixels)",
                         showline=True,
                         linewidth=2,
                         linecolor='black',
                         dtick=100,
                         tickvals=list(range(600, 1601, 100)),
                         ticktext=[600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600],
                         ticks="outside",
                         tickwidth=1,
                         tickcolor='black',
                         ticklen=7)

    fig.update_layout(title="Graph Set " + str(index + 1) + " " + mouse + " Pupil Area vs Voltage Stim",
                      height=250 * 100,
                      width=1250,
                      plot_bgcolor="white")

    fig.write_html("graph_set_" + str(index + 1) + "_" + mouse + "_pupil_area_vs_voltage_stim.html")
    pio.write_image(fig, "graph_set_" + str(index + 1) + "_" + mouse + "_pupil_area_vs_voltage_stim.pdf")

    # Shows the first 5 Graph Sets to confirm everything is working as intended
    # if index < 5:
    #     fig.show()
    index = index + 1

# Now it is time to create the overall graph to observe trends

# Average area of each of the subplots
average_area = []
# Average stim value of each subplot
average_stim = []

# For i in length of 2 seconds (64)
for i in range(len(pupil_area_per_stim[0])):
    # For j in stims (2500)
    for j in range(len(pupil_area_per_stim)):
        # if first stim (list is empty)
        if j == 0:
            # append first stim value of i ms
            average_area.append(pupil_area_per_stim[j].iloc[i])
        else:
            # insert at i ms, the value originally and current stim value of that ms
            average_area[i] = average_area[i] + pupil_area_per_stim[j].iloc[i]
    # divide i ms by total number of stims
    average_area[i] = average_area[i] / len(pupil_area_per_stim)

# Find average stims
for i in range(len(stims[0])):
    for j in range(len(stims)):
        if j == 0:
            average_stim.append(stims[j].iloc[i])
        else:
            average_stim[i] = average_stim[i] + stims[j].iloc[i]
    average_stim[i] = average_stim[i] / len(stims)

# Reshape the average area so we can standardize it
average_area_array = np.array(average_area).reshape(-1, 1)

# Standardizes Average Pupil Area and saves into dataframe
scaler = StandardScaler()
stan_area_df = pd.DataFrame(data=scaler.fit_transform(average_area_array), columns=['average_area'])

# Calculate mean, standard deviation, and Standard Error of Means for Pupil Area
mean = scaler.mean_
std = scaler.scale_
sem = std[0]/math.sqrt(len(average_area))

# Creating index list to pass in graph
area_index = list(stan_area_df.index)
# area_index = [x+1 for x in area_index]

# Creates Continuous Error Bars
area_upper = []
area_lower = []
for i in range(len(average_area)):
    area_upper.append(stan_area_df.iloc[i, 0] + sem)
    area_lower.append(stan_area_df.iloc[i, 0] - sem)

# Saves average stims into a dataframe
stim_df = pd.DataFrame(data=average_stim, columns=['average_stim'])

# Time to create the graph
fig = make_subplots()

fig.add_trace(
    go.Scatter(x=stan_area_df.index,
               y=stan_area_df.average_area,
               line=dict(color='black'),
               showlegend=True,
               name='Pupil Area',
               mode='lines'))
fig.add_trace(
    go.Scatter(x=stim_df.index,
               y=stim_df.average_stim,
               line=dict(color='#3BCEDE'),
               opacity=0.8,
               showlegend=True,
               mode='lines',
               name='Visual Stimulus',
               xaxis='x2',
               yaxis='y2'))
fig.add_trace(
    go.Scatter(
            x=area_index+area_index[::-1], # x, then x reversed
            y=area_upper+area_lower[::-1], # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(0,0,0,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False))

fig.update_layout(
    xaxis=dict(title_text="Time From Visual Stimulus (Seconds)",
               showline=True,
               linewidth=2,
               linecolor='black',
               tickvals=list(range(0, 129, 16)),
               ticktext=[-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2],
               ticks="outside",
               tickwidth=1,
               tickcolor='black',
               ticklen=7),
    yaxis=dict(title_text="Pupil Area " + "(Norm, Mean +/- SEm)",
               showline=True,
               linewidth=2,
               linecolor='black',
               ticks="outside",
               tickwidth=1,
               tickcolor='black',
               ticklen=7),
    xaxis2=dict(title='',
                tickvals=list(range(10, 11, 10)),
                ticktext=[''],
                overlaying='x',
                side='top'),
    yaxis2=dict(title='',
                tickvals=list(range(10, 11, 10)),
                ticktext=[''],
                overlaying='y',
                side='right'),

    title_text=mouse + ' Standardized Average Pupil Area vs Average Voltage Stim',
    height=500,
    width=1250,
    plot_bgcolor="white"
)

# Show and save interactive plot
# fig.show()
fig.write_html(mouse + "_multiaxes_minmax_average_onset_alignment.html")
pio.write_image(fig, mouse + "_multiaxes_minmax_average_onset_alignment.pdf")
