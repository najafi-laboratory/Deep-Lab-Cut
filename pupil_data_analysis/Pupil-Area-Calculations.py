import pandas as pd
import numpy as np

# Read the file
file_name = "FN16_P_20240626_js_t_cam0_run007_20240624_141059DLC_resnet50_PupilPerimeterTrackAug28shuffle1_500000_filtered.csv"
data = pd.read_csv(file_name)


# Define a function to calculate the area using the Shoelace formula
def shoelace_formula(coords):
    x = coords['x'].astype(float).values
    y = coords['y'].astype(float).values

    # Ensure the polygon is closed by appending the first point to the end
    x = list(x) + [x[0]]
    y = list(y) + [y[0]]

    # Apply Shoelace formula
    area = 0.5 * abs(sum(x[i] * y[i + 1] - y[i] * x[i + 1] for i in range(len(x) - 1)))

    return area


# Drop extra rows and columns
data = data.drop(columns=["scorer"])
data = data.drop([0, 1])
data.reset_index(drop=True, inplace=True)

# Get the coordinates
coordinate_cols_x = data.columns[::3]
coordinate_cols_y = data.columns[1::3]

areas = []

# Calculate the area for each row
for index, row in data.iterrows():
    coords = pd.DataFrame({
        'x': row[coordinate_cols_x].values,
        'y': row[coordinate_cols_y].values
    })
    area = shoelace_formula(coords)
    areas.append(area)

area = pd.DataFrame()
area["area"] = areas

area.to_csv("area_per_frame.csv")

#
# # Function to calculate the average area for every 30 rows
# def calculate_average_area(area, window_size=30):
#     # Calculate the number of windows
#     num_windows = (len(area) + window_size - 1) // window_size  # Ceiling division
#
#     # Calculate the average area for each window
#     averages = [area.iloc[i * window_size:(i + 1) * window_size]['area'].mean() for i in range(num_windows)]
#
#     return averages
#
#
# # Calculate the average area for every 30 rows
# average_areas = calculate_average_area(area, window_size=30)
# average_area = pd.DataFrame()
# average_area["area"] = average_areas
# average_area.to_csv("area_per_second.csv")

