import pandas as pd
import os

input_folder = 'input_videos'
final_dataframe = pd.DataFrame()

# For every csv in the input folder
for file in os.listdir(input_folder):
    if file.endswith('.csv'):
        # Find file path and convert to dataframe
        file_path = os.path.join(input_folder, file)
        file_df = pd.read_csv(file_path)
        # Drop extra rows and columns
        file_df = file_df.drop(columns=["scorer"])
        file_df = file_df.drop([0, 1])        
        file_df = file_df.iloc[1:]
        file_df.reset_index(drop=True, inplace=True)
        # Concat with main dataset
        final_dataframe = pd.concat([final_dataframe, file_df], ignore_index=True)

final_dataframe.columns = ['xLeft', 'yLeft', 'probLeft', 'xTopLeft1', 'yTopLeft1', 'probTopLeft1', 
                           'xTopLeft2', 'yTopLeft2', 'probTopLeft2', 'xTop', 'yTop', 'probTop',
                           'xTopRight1', 'yTopRight1', 'probTopRight1', 'xTopRight2', 'yTopRight2', 'probTopRight2',
                           'xRight', 'yRight', 'probRight', 'xBottomRight1', 'yBottomRight1', 'probBottomRight1',
                           'xBottomRight2', 'yBottomRight2', 'probBottomRight2', 'xBottom', 'yBottom', 'probBottom',
                           'xBottomLeft1', 'yBottomLeft1', 'probBottomLeft1', 'xBottomLeft2', 'yBottomLeft2', 'probBottomLeft2',
                           'xEyeLeft', 'yEyeLeft', 'probEyeLeft', 'xEyeTopLeft1', 'yEyeTopLeft1', 'probEyeTopLeft1', 
                           'xEyeTopLeft2', 'yEyeTopLeft2', 'probEyeTopLeft2', 'xEyeTop', 'yEyeTop', 'probEyeTop',
                           'xEyeTopRight1', 'yEyeTopRight1', 'probEyeTopRight1', 'xEyeTopRight2', 'yEyeTopRight2', 'probEyeTopRight2',
                           'xEyeRight', 'yEyeRight', 'probEyeRight', 'xEyeBottomRight1', 'yEyeBottomRight1', 'probEyeBottomRight1',
                           'xEyeBottomRight2', 'yEyeBottomRight2', 'probEyeBottomRight2', 'xEyeBottom', 'yEyeBottom', 'probEyeBottom',
                           'xEyeBottomLeft1', 'yEyeBottomLeft1', 'probEyeBottomLeft1', 'xEyeBottomLeft2', 'yEyeBottomLeft2', 'probEyeBottomLeft2',
                           'xCenter', 'yCenter', 'probCenter']
                           
final_dataframe.to_csv('total_session_pupil_data.csv')