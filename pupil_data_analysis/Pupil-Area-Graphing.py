import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

avg = pd.read_csv('pupil_data_analysis/FN13_js_self/area_per_frame.csv')
y = []

# Removing Outliers
i = 0
# for index, row in avg.iterrows():
#     if row[1] > 1600 or row[1] < 700 and i > 5:
#         y.append(0.33 * y[-3] + 0.33 * y[-2] + 0.33 * y[-1])
#         i += 1
#     else:
#         y.append(row[1])
# df = pd.DataFrame()
# df['area'] = y

# Create an interactive plot using Plotly
fig = px.line(avg, y='area', title='FN13 20240618 Pupil Area per Frame')
fig.update_xaxes(title_text='Frame')
fig.update_yaxes(title_text='Area (Pixels)')

# Show the interactive plot
fig.show()
# fig.write_html("area_per_frame_no_outliers.html")

# df.to_csv("area_per_frame_no_outliers.csv")