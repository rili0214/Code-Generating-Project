import json

def save_intermediate_results(model_name, analysis_result, phase):
        filename = f"results/intermediate/{model_name}_{phase}_analysis.json"
        with open(filename, 'w') as f:
            json.dump(analysis_result, f)
            
def save_combined_json(file1_path, file2_path, output_path):
    """
    Combines two JSON files into one and saves the result to a specified output path.

    Parameters:
        file1_path (str): Path to the first JSON file.
        file2_path (str): Path to the second JSON file.
        output_path (str): Path to save the combined JSON file.

    Returns:
        dict: The combined JSON object.
    """
    # Ensure paths are strings
    file1_path, file2_path, output_path = map(str, [file1_path, file2_path, output_path])

    # Load the first JSON file
    with open(file1_path, 'r') as f1:
        result1 = json.load(f1)
        
    # Load the second JSON file
    with open(file2_path, 'r') as f2:
        result2 = json.load(f2)
        
    # Combine the JSON objects
    if isinstance(result1, dict) and isinstance(result2, dict):
        combined_json = {}
        combined_json["model 1"] = result1
        combined_json["model 2"] = result2
    elif isinstance(result1, list) and isinstance(result2, list):
        combined_json = result1 + result2
    else:
        raise ValueError("Unsupported JSON structures: both files must have the same root type.")
        
    # Save the combined JSON to the output path
    with open(output_path, 'w') as f:
        json.dump(combined_json, f, indent=4)

    return combined_json


if __name__ == "__main__":
     file1_path = "results/intermediate/llama_analysis.json"
     with open(file1_path, 'r') as f:
        result1 = json.load(f)
     print(result1)
     file2_path = "results/intermediate/qwen_analysis.json"
     with open(file2_path, 'r') as f:
        result2 = json.load(f)
     print(result2)
     output_path = "results/intermediate/combined_analysis.json"
     save_combined_json(file1_path, file2_path, output_path)
     with open(output_path, 'r') as f:
        result3 = json.load(f)
     print(result3)