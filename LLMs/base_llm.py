import json
import logging
from huggingface_hub import InferenceClient
from pathlib import Path

# Logging Configuration
log_file_path = Path(__file__).parent.parent / 'logs' / 'app.log'
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration Constants
API_TOKEN_qwen = "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" 
API_TOKEN_llama = "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"
API_TOKEN_phi = "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"
client = InferenceClient(api_key=API_TOKEN_qwen)

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
    try:
        stream = client.chat.completions.create(
            model=model_name,
            messages=messages,
            #max_tokens=10000,
            max_tokens=3000, 
            stream=True
        )

        complete_response = ""
        for chunk in stream:
            if 'choices' in chunk and 'delta' in chunk['choices'][0]:
                content = chunk['choices'][0]['delta'].get('content', '')
                complete_response += content
                print(content, end="", flush=True)
            else:
                logger.warning(f"Unexpected chunk format: {chunk}")
        
        logger.info("Completed Hugging Face API call with response.")
        return complete_response

    except Exception as e:
        logger.error(f"Error in Hugging Face API call: {e}")
        raise

def save_response_to_json(response, model, call_type):
    """Saves response to a JSON file with a timestamped filename."""
    output_path = Path(__file__).parent.parent / 'results' / f"{model}_results" / f"{call_type}_results.json"
    try:
        with open(output_path, 'w') as file:
            json.dump({"response": response}, file, indent=4)
        logger.info(f"Response saved to {output_path}")
    except Exception as e:
        logger.error(f"Error saving response to JSON: {e}")