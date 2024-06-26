from sklearn.preprocessing import minmax_scale
import pandas as pd
import numpy as np
import plotly.express as px

area_per_frame = pd.DataFrame(pd.read_csv("area_per_frame_no_outliers.csv").iloc[:,1])

normalized_area = pd.DataFrame(minmax_scale(area_per_frame), columns=['Area'])

normalized_area.to_csv("minmax_scale.csv")