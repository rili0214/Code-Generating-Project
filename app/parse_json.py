#############################################################################################################################
# Program: parse_json.py                                                                                                    #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program defines helper functions for saving and combining JSON files.                                   #                                                                                                 
#############################################################################################################################

import json

def save_intermediate_results(model_name, analysis_result, phase):
        """
        Saves intermediate analysis results to a JSON file.

        paras:
            model_name (str): Name of the model.
            analysis_result (dict): Analysis results to be saved.
            phase (str): Phase of the analysis (e.g., "initial" or "feedback").

        effects:
            Creates a JSON file named "{model_name}_{phase}_analysis.json" in the "results/intermediate" directory.
        """
        filename = f"results/intermediate/{model_name}_{phase}_analysis.json"
        with open(filename, 'w') as f:
            json.dump(analysis_result, f)
            
def save_combined_json(file1_path, file2_path, output_path):
    """
    Combines two JSON files into one and saves the result to a specified output path.

    paras:
        file1_path (str): Path to the first JSON file.
        file2_path (str): Path to the second JSON file.
        output_path (str): Path to save the combined JSON file.

    returns:
        dict: The combined JSON object.

    effects:
        Reads the contents of the first and second JSON files.
        Combines the contents of the two files into a single JSON object.
        Saves the combined JSON object to the specified output path.

    raises:
        ValueError: If the root type of both JSON files is not the same.
    """
    file1_path, file2_path, output_path = map(str, [file1_path, file2_path, output_path])

    with open(file1_path, 'r') as f1:
        result1 = json.load(f1)

    with open(file2_path, 'r') as f2:
        result2 = json.load(f2)

    if isinstance(result1, dict) and isinstance(result2, dict):     # Check if both files are dictionaries
        combined_json = {}
        combined_json["model 1"] = result1
        combined_json["model 2"] = result2
    elif isinstance(result1, list) and isinstance(result2, list):   # Check if both files are lists
        combined_json = result1 + result2
    else:
        raise ValueError("Unsupported JSON structures: both files must have the same root type.")
 
    with open(output_path, 'w') as f:
        json.dump(combined_json, f, indent = 4)

    return combined_json