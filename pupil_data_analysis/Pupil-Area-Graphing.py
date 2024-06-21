import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

avg = pd.read_csv("area_per_frame.csv")
y = []

# Removing Outliers
for index, row in avg.iterrows():
    if row[1] > 1750 or row[1] < 550:
        y.append(0.33 * y[-3] + 0.33 * y[-2] + 0.33 * y[-1])
    else:
        y.append(row[1])
df = pd.DataFrame()
df['area'] = y

# Create an interactive plot using Plotly
fig = px.line(df, y='area', title='VG01 20240515 Pupil Area per Frame')
fig.update_xaxes(title_text='Frame')
fig.update_yaxes(title_text='Area (Pixels)')

# Show the interactive plot
fig.show()
fig.write_html("area_per_frame_no_outliers.html")

df.to_csv("area_per_frame_no_outliers.csv")