import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go


<<<<<<< HEAD
def write_graph_simulations(likelihoods, results_dir, session_name):
=======
def write_graph_simulations(likelihoods, results_dir):
>>>>>>> 7e06a49651f4c87ca61be24936f7260e27fc5b69
    graph_simulations = go.Figure()
    
    for column in likelihoods.columns:
        graph_simulations.add_trace(go.Scatter(x=likelihoods.index, y=likelihoods[column], mode='lines', name=str(df.loc[0,column])))
    
    graph_simulations.update_layout(
        title="Likelihoods over Time",
        xaxis_title="Index",
        yaxis_title="Likelihoods",
        showlegend=True
    )
    
<<<<<<< HEAD
    graph_simulations.write_html(f'{results_dir}/{session_name}_graph_simulations.html')
    

# plot the distribution of confidence levels, across all frames, for all body parts
def write_likelihoods_allBodyParts(likelihoods, results_dir, session_name):
=======
    graph_simulations.write_html(f'{results_dir}/graph_simulations.html')
    

# plot the distribution of confidence levels, across all frames, for all body parts
def write_likelihoods_allBodyParts(likelihoods, results_dir):
>>>>>>> 7e06a49651f4c87ca61be24936f7260e27fc5b69
    likelihoods_rounded = likelihoods.map(
        lambda x: round(float(x), 2) if isinstance(x, (int, float, str)) else x
    )
    likelihoods_rounded = likelihoods_rounded.melt(value_name="value")["value"]
    
    freq_map = likelihoods_rounded.value_counts()
    
    freq_map_df = freq_map.reset_index()
    freq_map_df.columns = ['Confidence Level', 'Frequency']
    freq_map_df = freq_map_df.sort_values(by='Confidence Level', ascending=False)
    
    # Normalize frequencies to create a probability distribution
    freq_map_df['Probability'] = freq_map_df['Frequency'] / freq_map_df['Frequency'].sum()
    
    # Plot the probability distribution function
    fig1 = px.line(
        freq_map_df,
        x='Confidence Level',
        y='Probability',
        title='Frequency of Confidence Probability Distribution Function',
        labels={'Confidence Level': 'Confidence Level', 'Probability': 'Probability'}
    )
    
<<<<<<< HEAD
    fig1.write_html(f'{results_dir}/{session_name}_confidence_plot_allBodyParts.html')
    

# plot the distribution of confidence levels, across all frames, for individual body parts
def write_likelihoods_eachBodyPart(likelihoods, results_dir, session_name):
=======
    fig1.write_html(f'{results_dir}/confidence_plot_allBodyParts.html')
    


#%%# plot the distribution of confidence levels, across all frames, for individual body parts

def write_likelihoods_eachBodyPart(likelihoods, results_dir):
>>>>>>> 7e06a49651f4c87ca61be24936f7260e27fc5b69

    fig1 = go.Figure()

    for column in likelihoods.columns:

        likelihoods_rounded = likelihoods[column].map(
            lambda x: round(float(x), 2) if isinstance(x, (int, float, str)) else x
        )
        # likelihoods_rounded = likelihoods_rounded.melt(value_name="value")["value"]
        
        freq_map = likelihoods_rounded.value_counts()
        
        freq_map_df = freq_map.reset_index()
        freq_map_df.columns = ['Confidence Level', 'Frequency']
        freq_map_df = freq_map_df.sort_values(by='Confidence Level', ascending=False)
        

        # Normalize frequencies to create a probability distribution
        freq_map_df['Probability'] = freq_map_df['Frequency'] / freq_map_df['Frequency'].sum()
        


        fig1.add_trace(go.Scatter(x=freq_map_df['Confidence Level'], y=freq_map_df['Probability'], mode='lines', name=str(df.loc[0,column])))


    fig1.update_layout(
            title="Frequency of Confidence Probability Distribution Function",
            xaxis_title='Confidence Level',
            yaxis_title='Probability',
            showlegend=True
        )
        

<<<<<<< HEAD
    fig1.write_html(f'{results_dir}/{session_name}_confidence_plot_eachBodyPart.html')
=======
    fig1.write_html(f'{results_dir}/confidence_plot_eachBodyPart.html')
>>>>>>> 7e06a49651f4c87ca61be24936f7260e27fc5b69






if __name__ == "__main__":
<<<<<<< HEAD

    path_to_model_output_folder = "" #"/storage/home/hcoda1/8/fnajafi3/r-fnajafi3-0/DLC/Model/Track-GroupName-2025-11-08/output"
    results_dir = "" # path_to_postproc_results_foler #"/storage/home/hcoda1/8/fnajafi3/r-fnajafi3-0/DLC/postproc/results"

    csv_dir_all = [d for d in os.listdir() if d.endswith('.csv')]
=======

    path_to_output_folder = "" #"/storage/home/hcoda1/8/fnajafi3/r-fnajafi3-0/DLC/Model/Track-GroupName-2025-11-08/output"
    
    csv_dir_all = [for d in os.listdir() if d.endswith('csv')]
    
    results_dir = "" # path_to_postproc_results_foler #"/storage/home/hcoda1/8/fnajafi3/r-fnajafi3-0/DLC/Post_processing/Results"
>>>>>>> 7e06a49651f4c87ca61be24936f7260e27fc5b69

    for csv_dir in csv_dir_all:
        # csv_dir = "/storage/home/hcoda1/8/fnajafi3/r-fnajafi3-0/DLC/Model/Body_tracking-Group Name-2025-11-05/output/yh24lg-trialvid-9-2025-10-23-120924-compressed_bGZTDDTRDLC_HrnetW48_Body_trackingNov5shuffle1_detector_best-100_snapshot_best-10.csv"	
        
        df = pd.read_csv(csv_dir)
<<<<<<< HEAD
        likelihoods = df.iloc[2:, list(range(3, len(df.columns), 3))]

        session_name = csv_dir.split("_HrnetW48")[0]
        
        write_graph_simulations(likelihoods, results_dir, session_name)
        write_likelihoods_allBodyParts(likelihoods, results_dir, session_name)
        write_likelihoods_eachBodyPart(likelihoods, results_dir, session_name)
=======
    
    
        likelihoods = df.iloc[2:, list(range(3, len(df.columns), 3))]
        
        write_graph_simulations(likelihoods, results_dir)
        write_likelihoods_allBodyParts(likelihoods, results_dir)
        write_likelihoods_eachBodyPart(likelihoods, results_dir)
>>>>>>> 7e06a49651f4c87ca61be24936f7260e27fc5b69
