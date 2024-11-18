import pandas as pd
import numpy as np

# Read the file
file_name = "total_session_pupil_data.csv"
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
data = data.drop([0])
data.reset_index(drop=True, inplace=True)

# Get the coordinates
coordinate_cols_x = data.columns[1::3]
coordinate_cols_y = data.columns[2::3]

pupil_cols_x = coordinate_cols_x[:12]
eye_cols_x = coordinate_cols_x[12:24]

pupil_cols_y = coordinate_cols_y[:12]
eye_cols_y = coordinate_cols_y[12:24]

pupil_areas = []
eye_areas = []

# Calculate the area for each row
for index, row in data.iterrows():
    pupil_coords = pd.DataFrame({
        'x': row[pupil_cols_x].values,
        'y': row[pupil_cols_y].values
    })
    eye_coords = pd.DataFrame({
        'x': row[eye_cols_x].values,
        'y': row[eye_cols_y].values
    })
    pupil_area = shoelace_formula(pupil_coords)
    eye_area = shoelace_formula(eye_coords)
    pupil_areas.append(pupil_area)
    eye_areas.append(eye_area)
    if index % 1000 == 0:
        print('Index:', index, 'Total:', len(data))

area = pd.DataFrame()
area["Pupil_Area"] = pupil_areas
area['Eye_Area'] = eye_areas
area['Center_X'] = data.iloc[:, 73]
area['Center_Y'] = data.iloc[:, 74]

area.to_csv("sleep_DLC_analysis.csv")