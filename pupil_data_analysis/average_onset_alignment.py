from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Removes outliers from the data
area = pd.read_csv("area_per_frame.csv")
y = []
for index, row in area.iterrows():
    if row[1] > 1750 or row[1] < 600:
        y.append(0.33 * y[-3] + 0.33 * y[-2] + 0.33 * y[-1])
    else:
        y.append(row[1])
area_per_frame = pd.DataFrame()
area_per_frame['area'] = y

frame_times = pd.read_excel("../2p_camlog_alignment/voltage_camlog_frames_aligned.xlsx").iloc[:, 2]
voltage = pd.read_csv("../2p_camlog_alignment/voltage.csv")

voltage_stim = []

last_stim = 0

# Calculates whenever voltage stim turns on and saves to list
for index, row in voltage.iterrows():
    if row["vol_stim"] == 1 and row["vol_stim"] != last_stim:
        voltage_stim.append(row["time"])
        last_stim = 1
    elif row["vol_stim"] != last_stim:
        last_stim = 0

j = 0

pupil_area_per_stim = []
pupil_stim_frames = []

# # saves all the pupil data 2 seconds before and 2 seconds after stim onset time
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

average_area = []

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

average_area_array = np.array(average_area).reshape(-1, 1)

scaler = StandardScaler()
area_df = pd.DataFrame(data=scaler.fit_transform(average_area_array),columns=['average_area'])
#area_df = pd.DataFrame(data=average_area_array,columns=['average_area'])

voltage = np.full(len(pupil_area_per_stim[0]), 0)
for i in range(6):
    voltage[64 + i] = 1

fig = go.Figure()

fig.add_trace(go.Scatter(x=area_df.index, y=area_df.average_area, line=dict(color='black'), showlegend=False))
fig.add_trace(go.Scatter(x=list(range(len(voltage))), y=voltage, line=dict(color='green'), showlegend=False))

fig.update_xaxes(title_text="Time (Seconds)", showline=True, linewidth=2, linecolor='black',
                         tickvals=list(range(0, 129, 16)),
                         ticktext=[-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2], ticks="outside", tickwidth=1,
                         tickcolor='black', ticklen=7)
fig.update_yaxes(title_text="Area in Pixels (Standardized)", showline=True, linewidth=2, linecolor='black',
                         ticks="outside", tickwidth=1, tickcolor='black', ticklen=7)

fig.update_layout(title="VG01 20240517 Standardized Average Pupil Area vs Voltage Stim", height=500, width=1250, plot_bgcolor="white")

# Show the interactive plot
fig.show()
fig.write_html("standardized_average_onset_alignment.html")