import json

def save_intermediate_results(model_name, analysis_result, phase):
        filename = f"results/intermediate/{model_name}_{phase}_analysis.json"
        with open(filename, 'w') as f:
            json.dump(analysis_result, f)
            
def save_combined_json(self, file1_path, file2_path, output_path):
    """
    Combines two JSON files into one and saves the result to a specified output path.

    Parameters:
        file1_path (str): Path to the first JSON file.
        file2_path (str): Path to the second JSON file.
        output_path (str): Path to save the combined JSON file.

    Returns:
    dict: The combined JSON object.
    """
    # Load the first JSON file
    with open(file1_path, 'r') as f1:
        result1 = json.load(f1)
        
    # Load the second JSON file
    with open(file2_path, 'r') as f2:
        result2 = json.load(f2)
        
    # Combine the two JSON objects
    combined_json = {**result1, **result2}
        
    # Save the combined JSON to the output path
    with open(output_path, 'w') as f:
        json.dump(combined_json, f, indent=4)  # Pretty-print with an indent

    return combined_json