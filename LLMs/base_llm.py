import json
from huggingface_hub import InferenceClient
from pathlib import Path
from logs import setup_logger

# Logging Configuration
logger = setup_logger()

# Configuration Constants
API_TOKEN_qwen = "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"
API_TOKEN_llama = "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"
API_TOKEN_phi = "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"
AZURE_OPENAI_API_KEY = ""  
AZURE_OPENAI_ENDPOINT = ""
AZURE_OPENAI_DEPLOYMENT = ""  
AZURE_API_VERSION = ""

client = InferenceClient(api_key=API_TOKEN_qwen)

system_prompt = """
You are a highly accurate and efficient debugging assistant. Your sole task is to generate the corrected 
version of the given code. Do not provide explanations, comments, or any additional text. Respond with 
only the debugged code wrapped in proper markdown backticks.

Follow these rules strictly:
1. Only produce the debugged code.
2. Use the input code's formatting and style unless otherwise specified.
3. Ensure the code is syntactically correct and logically consistent.

All responses must adhere to this format: ```debugged code```


If the input is invalid or incomplete, produce the best debugged code you can infer based on the given input. 
Do not state assumptions; simply adjust the code directly.
"""

user_prompt = """
Fix all bugs in the code. Ensure that it runs without errors and achieves the intended functionality. Return 
only the debugged code in this format: ```debugged code```
"""

qwen_system_prompt_initial = """
You are an expert software debugging assistant specializing in identifying and fixing errors in programming 
code. Your task is to analyze buggy code provided by the user, identify potential issues, and generate an 
enhanced version of the code that fixes these issues. You only need to provide the corrected code. No 
explanations or comments should be included.

To achieve this, please follow these steps:

1. Understand the provided code and identify areas that may cause bugs or inefficiencies.
2. Apply your debugging expertise to generate corrected code. Ensure the solution is efficient, adheres to 
standard coding practices, and resolves any evident errors.
3. Avoid adding explanations or commentary; return only the corrected code for immediate use.

The input may involve different programming languages, so ensure your solution is tailored to the language 
detected. Always prioritize correctness and maintain readability. Your response must adhere to this 
format: ```debugged code```
"""

qwen_user_prompt_initial = """
The buggy code snippet is provided below. Please debug it and provide a corrected version in the same 
programming language without explanations. Ensure the code adheres to the format: ```debugged code``` and 
is free of syntax, logical, or runtime errors.  
"""

qwen_system_prompt_feedback = """
You are a execellent debugging assistant specializing in advanced code debugging using additional analysis 
results. You have access to combined outputs from multiple models, including static analysis, dynamic 
analysis, formal verification data, and performance evaluations.

Your goal is to:

1. Evaluate the provided JSON file containing analysis data and determine which model’s generated code is 
superior based on the final_score.
2. Incorporate this information to enhance the debugged code, ensuring it integrates the best features from 
the higher-scored model. If the other models have lower score, you may check their code to see if you 
can use some of their features to improve your code.

Follow these steps:
Step 1: Analyze the additional data in the JSON file to identify potential bugs and improvement areas.
Step 2: Combine insights from static analysis, dynamic analysis, and formal verification to generate the 
most robust and efficient code possible.

Your response should only include the enhanced debugged code. Commentary or explanations are not needed unless 
explicitly requested by the user. Prioritize integrating high-scoring solutions while ensuring that the 
generated code adheres to best practices, is efficient, and resolves all detected issues.
"""

qwen_user_prompt_feedback = """
You are provided with buggy code and an additional JSON file containing results from multiple models, including 
their evaluations and analysis.

Identify which model performed better by comparing the final_score values in the JSON data.
Debug and enhance the provided code using insights from the higher-scored model and the additional analyses.

In this response, you may include explanations if needed. However, you must adhere to the format: 

```debugged code```
Explnations  
"""

dafny_system_prompt = """You are an expert in formal verification and Dafny programming."""

dafny_user_prompt = """
Convert the following buggy code into correct code first, then generate Dafny for formal verification for the 
correct code. Ensure that the Dafny code includes contracts such as preconditions, postconditions, and 
invariants to verify the correctness of the program. Provide only valid Dafny code without explanations.
"""

qwen_final_report_system_prompt = """
You are a helpful and detail-oriented code analysis assistant. You will take in a JSON file containing evaluation 
results from various code analysis tools (such as static analysis, Valgrind, formal verification, and RankMe) and 
generate the following:
1. A concise summary of the evaluation results for each included tool.
2. A final evaluation score summary, highlighting key strengths and weaknesses.
3. Actionable tips on how the code can be improved, including specific steps and examples.

Your output should be clear, organized, and constructive to help improve code quality and performance effectively.
"""

qwen_final_report_user_prompt = """
Given the following evaluation results JSON file, summarize the evaluation and provide actionable tips on how to 
improve the code quality and score. Include:
1. A summary of analysis results for each included tool (e.g., static analysis, Valgrind, formal verification, 
RankMe).
2. Highlights of key issues or strengths.
3. Specific suggestions to fix issues or improve the code, with examples where applicable.
"""

def load_json_data(json_path):
    """Loads additional data from a JSON file."""
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
        logger.info(f"Loaded data from {json_path}")
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {json_path}")
        return None
    except json.JSONDecodeError:
        logger.error(f"JSON decode error in file: {json_path}")
        return None

def prepare_messages(system_prompt, user_prompt, code_snippet=None, additional_data=None):
    """Prepare message prompts for the Hugging Face model."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    if code_snippet:
        messages.append({"role": "user", "content": f"Here is the code snippet:\n\n{code_snippet}"})

    if additional_data:
        messages.append({"role": "system", "content": json.dumps(additional_data)})
    
    logger.info("Messages prepared successfully.")
    return messages

def call_huggingface_chat(model_name, messages):
    """Call the Hugging Face API to generate code."""
    if model_name == "Qwen/Qwen2.5-Coder-32B-Instruct":
        stream = client.chat.completions.create(
            model = model_name,
            messages = messages,
            max_tokens = 1000,
            stream = True
        )
    else:
        stream = client.chat.completions.create(
            model = model_name,
            messages = messages,
            max_tokens = 500, 
            stream = True
        )
    try:
        complete_response = ""
        for chunk in stream:
            if 'choices' in chunk and 'delta' in chunk['choices'][0]:
                content = chunk['choices'][0]['delta'].get('content', '')
                complete_response += content
            else:
                logger.warning(f"Unexpected chunk format: {chunk}")
        
        logger.info("Completed Hugging Face API call with response.")
        return complete_response

    except Exception as e:
        logger.error(f"Error in Hugging Face API call: {e}")
        raise

def save_response_to_json(mode, model, generated_code, call_type, language):
    """Saves response to a JSON file with a timestamped filename."""
    output_path = Path(__file__).parent.parent / 'results' / f"{model}_results" / f"{call_type}_results.json"
    try:
        temp = {}
        temp["mode"] = mode
        temp["model"] = model
        temp["generated_code"] = generated_code
        temp["language"] = language
        temp["dafny_text"] = ""
        with open(output_path, 'w') as file:
            json.dump(temp, file, indent=4)
        logger.info(f"Response saved to {output_path}")
    except Exception as e:
        logger.error(f"Error saving response to JSON: {e}")

def save_response_to_txt(response, path):
    """Saves response to a text file with a timestamped filename."""
    try:
        with open(path, 'w') as file:
            file.write(response)
        logger.info(f"Response saved to {path}")
    except Exception as e:
        logger.error(f"Error saving response to text file: {e}")