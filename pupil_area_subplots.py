from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

data = pd.read_csv("area_per_second.csv")
y = []

# Removing Outliers
for index, row in data.iterrows():
    if row[1] > 1750 or row[1] < 600:
        y.append(0.33 * y[-3] + 0.33 * y[-2] + 0.33 * y[-1])
    else:
        y.append(row[1])
df = pd.DataFrame()
df['area'] = y

# df = data

fig = make_subplots(rows=3, cols=1)

fig.append_trace(go.Scatter(
    x=list(range(len(data)//3)),
    y=df["area"].iloc[:len(data)//3],
    showlegend=False,
    line=dict(color='black'),
), row=1, col=1)

fig.append_trace(go.Scatter(
    x=list(range(len(data)//3, 2*len(data)//3)),
    y=df["area"].iloc[len(data)//3:2*len(data)//3],
    showlegend=False,
    line=dict(color='black'),
), row=2, col=1)

fig.append_trace(go.Scatter(
    x=list(range(2*len(data)//3, len(data))),
    y=df["area"].iloc[int(2*len(data)/3):],
    showlegend=False,
    line=dict(color='black'),
), row=3, col=1)


fig.update_layout(height=700, width=1300, title_text="VG01 20240517 Area (Pixel) Per Second", plot_bgcolor="whitesmoke", xaxis_title="Seconds", yaxis_title="Area (Pixel)")

fig.show()
# fig.write_image("VG01_20240517_Area_Per_Frame.pdf", format="pdf")
