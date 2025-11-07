import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go


def write_graph_simulations(likelihoods, output_dir):
    graph_simulations = go.Figure()
    
    for column in likelihoods.columns:
        graph_simulations.add_trace(go.Scatter(x=likelihoods.index, y=likelihoods[column], mode='lines', name=str(df.loc[0,column])))
    
    graph_simulations.update_layout(
        title="Likelihoods over Time",
        xaxis_title="Index",
        yaxis_title="Likelihoods",
        showlegend=True
    )
    
    graph_simulations.write_html(f'{output_dir}/graph_simulations.html')
    

# plot the distribution of confidence levels, across all frames, for all body parts
def write_likelihoods_allBodyParts(likelihoods, output_dir):
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
    
    fig1.write_html(f'{output_dir}/confidence_plot_allBodyParts.html')
    


#%%# plot the distribution of confidence levels, across all frames, for individual body parts

def write_likelihoods_eachBodyPart(likelihoods, output_dir):

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
        

    fig1.write_html(f'{output_dir}/confidence_plot_eachBodyPart.html')






if __name__ == "__main__":
    # csv_dir = ""
    # output_dir = ""

    csv_dir = "/storage/home/hcoda1/8/fnajafi3/r-fnajafi3-0/DLC/Model/Body_tracking-Group Name-2025-11-05/output/yh24lg-trialvid-9-2025-10-23-120924-compressed_bGZTDDTRDLC_HrnetW48_Body_trackingNov5shuffle1_detector_best-100_snapshot_best-10.csv"	
    output_dir = "/storage/home/hcoda1/8/fnajafi3/r-fnajafi3-0/DLC/Post_processing/Results"

    
    df = pd.read_csv(csv_dir)


    likelihoods = df.iloc[2:, list(range(3, len(df.columns), 3))]
    
    write_graph_simulations(likelihoods, output_dir)
    write_likelihoods_allBodyParts(likelihoods, output_dir)
    write_likelihoods_eachBodyPart(likelihoods, output_dir)
