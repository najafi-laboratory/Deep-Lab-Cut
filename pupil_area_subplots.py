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


fig.update_layout(height=650, width=1250, title_text="VG01 20240517 Area (Pixel) Per Second", plot_bgcolor="white")

fig.update_xaxes(row=1, col=1, title_text="Seconds", showline=True, linewidth=2, linecolor='black', dtick=50, tickvals = list(range(0, 1101, 50)), ticktext=[0, " ", 100, " ", 200, " ", 300, " ", 400, " ", 500, " ", 600, " ", 700, " ", 800, " ", 900, " ", 1000, " ", 1100], ticks="outside", tickwidth=1, tickcolor='black', ticklen=7)
fig.update_yaxes(row=1, col=1, title_text="Area (Pixels)", showline=True, linewidth=2, linecolor='black', dtick=100, tickvals = list(range(800, 1601, 100)), ticktext=[800, " ", 1000, " ", 1200, " ", 1400, " ", 1600], ticks="outside", tickwidth=1, tickcolor='black', ticklen=7)

fig.update_xaxes(row=2, col=1, title_text="Seconds", showline=True, linewidth=2, linecolor='black', dtick=50, tickvals = list(range(1150, 2251, 50)), ticktext=[" ", 1200, " ", 1300, " ", 1400, " ", 1500, " ", 1600, " ", 1700, " ", 1800, " ", 1900, " ", 2000, " ", 2100, " ", 2200, " "], ticks="outside", tickwidth=1, tickcolor='black', ticklen=7)
fig.update_yaxes(row=2, col=1, title_text="Area (Pixels)", showline=True, linewidth=2, linecolor='black', dtick=100, tickvals = list(range(800, 1601, 100)), ticktext=[800, " ", 1000, " ", 1200, " ", 1400, " ", 1600], ticks="outside", tickwidth=1, tickcolor='black', ticklen=7)

fig.update_xaxes(row=3, col=1, title_text="Seconds", showline=True, linewidth=2, linecolor='black', dtick=50, tickvals = list(range(2300, 3401, 50)), ticktext=[2300, " ", 2400, " ", 2500, " ", 2600, " ", 2700, " ", 2800, " ", 2900, " ", 3000, " ", 3100, " ", 3200, " ", 3300, " ", 3400], ticks="outside", tickwidth=1, tickcolor='black', ticklen=7)
fig.update_yaxes(row=3, col=1, title_text="Area (Pixels)", showline=True, linewidth=2, linecolor='black', dtick=100, tickvals = list(range(800, 1601, 100)), ticktext=[800, " ", 1000, " ", 1200, " ", 1400, " ", 1600], ticks="outside", tickwidth=1, tickcolor='black', ticklen=7)

fig.show()
# fig.write_image("VG01_20240517_Area_Per_Frame.pdf", format="pdf")
