# Validation.py

## Overview
This script processes DeepLabCut model output and generates interactive visualizations to validate pose detection confidence levels. It analyzes the likelihood (confidence) values for tracked body parts across video frames.

## Purpose
The script creates three types of HTML visualizations to assess the quality and reliability of pose estimation:
1. **Likelihood over Time**: Track how confidence scores change throughout the video
2. **Confidence Distribution (All Body Parts)**: View the overall confidence distribution across all tracked body parts
3. **Confidence Distribution (Individual Body Parts)**: Compare confidence distributions for each body part separately

## Functions

### `write_graph_simulations(likelihoods, results_dir, session_name)`
Generates an interactive line graph showing likelihood values over time for all body parts.

**Parameters:**
- `likelihoods`: DataFrame containing confidence/likelihood values
- `results_dir`: Output directory for HTML files
- `session_name`: Name to identify the session in output filenames

**Output:** `{session_name}_graph_simulations.html`

### `write_likelihoods_allBodyParts(likelihoods, results_dir, session_name)`
Creates a probability distribution plot showing the frequency of confidence levels across all body parts and frames.

**Parameters:**
- `likelihoods`: DataFrame containing confidence/likelihood values
- `results_dir`: Output directory for HTML files
- `session_name`: Name to identify the session in output filenames

**Output:** `{session_name}_confidence_plot_allBodyParts.html`

### `write_likelihoods_eachBodyPart(likelihoods, results_dir, session_name)`
Generates overlaid probability distribution plots for each individual body part, allowing comparison of confidence distributions across tracked features.

**Parameters:**
- `likelihoods`: DataFrame containing confidence/likelihood values
- `results_dir`: Output directory for HTML files
- `session_name`: Name to identify the session in output filenames

**Output:** `{session_name}_confidence_plot_eachBodyPart.html`

## Usage

1. Set the path variables in the `__main__` section:
   - `path_to_model_output_folder`: Directory containing DeepLabCut model output CSV files
   - `results_dir`: Directory where HTML visualizations will be saved

2. Run the script:
   ```bash
   python validation.py
   ```

3. The script will:
   - Find all CSV files in the model output folder
   - Extract likelihood columns from each CSV
   - Generate three HTML visualizations for each session
   - Save results to the specified results directory

## Input Format
Expects CSV files from DeepLabCut model output with the standard format where:
- Row 0-1: Header information
- Row 2+: Frame data
- Columns follow the pattern: `body_part_x`, `body_part_y`, `body_part_likelihood` (repeating for each body part)

## Dependencies
- `pandas`: Data manipulation and analysis
- `plotly.express`: Interactive visualizations
- `plotly.graph_objects`: Advanced graph construction
- `os`: File system operations

## Output
Interactive HTML files that can be opened in any web browser for detailed exploration of pose detection confidence metrics.

## Notes
- Confidence values are rounded to 2 decimal places for analysis
- All visualizations are interactive (zoom, pan, hover for details)
- The script processes all CSV files in the specified folder
