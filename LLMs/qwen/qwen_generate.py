import json
import logging
from huggingface_hub import InferenceClient
from pathlib import Path

# Logging Configuration
log_file_path = Path(__file__).parent.parent.parent / 'logs' / 'app.log'
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration Constants
API_TOKEN = "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" 
client = InferenceClient(api_key=API_TOKEN)

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

def call_huggingface_chat(messages):
    """Call Hugging Face API with streaming."""
    try:
        stream = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=messages,
            #max_tokens=500,
            stream=True
        )

        # Accumulate and print streaming response
        complete_response = ""
        for chunk in stream:
            # Check if 'choices' and 'delta' exist in the response
            if 'choices' in chunk and 'delta' in chunk['choices'][0]:
                content = chunk['choices'][0]['delta'].get('content', '')
                complete_response += content
                print(content, end="")
            else:
                # Log the chunk to inspect its structure
                logger.warning(f"Unexpected chunk format: {chunk}")
        
        logger.info("Completed Hugging Face API call with response.")
        return complete_response

    except Exception as e:
        logger.error(f"Error in Hugging Face API call: {e}")
        raise


def initial_call(code_):
    """Initial call without JSON data."""
    system_prompt = "You are a code debugging assistant."
    user_prompt = "Please fix the issues in the following code:"
    code_input = code_

    messages = prepare_messages(system_prompt, user_prompt, code_snippet=code_input)
    response = call_huggingface_chat(messages)
    return response

def feedback_call(code_, json_path):
    """Feedback call that includes additional JSON data."""
    system_prompt = "You are a code debugging assistant with additional analysis results."
    user_prompt = "Please enhance and debug the code with the given static, dynamic, and formal analysis results."
    code_input = code_

    additional_data = load_json_data(json_path)
    if not additional_data:
        logger.error("No additional data loaded. Aborting feedback call.")
        return None

    messages = prepare_messages(system_prompt, user_prompt, code_snippet=code_input, additional_data=additional_data)
    response = call_huggingface_chat(messages)
    return response

if __name__ == "__main__":
    # Call the initial function
    initial_call("def add(a, b): return a + b")

    # Example JSON path for feedback call
    json_file_path = Path(__file__).parent / 'data' / 'additional_data.json'
    #feedback_call(json_file_path)

    logger.info("Script execution completed.")