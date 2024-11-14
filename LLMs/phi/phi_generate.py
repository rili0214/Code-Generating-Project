"""

import json
import logging
from huggingface_hub import InferenceClient
from pathlib import Path
from LLMs.base_llm import API_TOKEN_llama, load_json_data, prepare_messages, call_huggingface_chat, save_response_to_json

json_file_path = Path(__file__).parent.parent.parent / 'results' / 'intermediate' / 'llama_analysis.json'

# Logging Configuration
log_file_path = Path(__file__).parent.parent / 'logs' / 'app.log'
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration Constants
client = InferenceClient(api_key=API_TOKEN_llama)

model = "microsoft/Phi-3-mini-128k-instruct"

def initial_call(code_):
    #Initial call without JSON data.
    system_prompt = "You are a code debugging assistant. Just give the debugged code. No need to explain your code!"
    user_prompt = "Please fix the issues in the following code:"
    code_input = code_

    messages = prepare_messages(system_prompt, user_prompt, code_snippet=code_input)
    response = call_huggingface_chat(model, messages)

    save_response_to_json(response, "llama", "llama_initial")

def feedback_call(code_, json_path):
    #Feedback call that includes additional JSON data.
    system_prompt = "You are a code debugging assistant with additional analysis results. Just give the debugged code. No need to explain your code!"
    user_prompt = "Please enhance and debug the code with the given static, dynamic, and formal analysis results."
    code_input = code_

    additional_data = load_json_data(json_path)
    if not additional_data:
        logger.error("No additional data loaded. Aborting feedback call.")
        return None

    messages = prepare_messages(system_prompt, user_prompt, code_snippet=code_input, additional_data=additional_data)
    print(messages)
    response = call_huggingface_chat(model, messages)

    save_response_to_json(response, "llama", "llama_feedback")

if __name__ == "__main__":
    #initial_call("def add(a, b): return a + b")
    
    feedback_call("def binary_search(arr, target):\n left = 0\n right = len(arr) - 1\n\n while left < right:\n mid = (left + right) <<1\n if arr[mid] == target:\n return mid\n elif arr[mid] < target:\n left = mid + 1\n else:\n right = mid - 1\n\n return -1", json_file_path)

    logger.info("LLaMa execution completed.")


"""
from huggingface_hub import InferenceClient

client = InferenceClient(api_key="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")

messages = [
	{
		"role": "user",
		"content": "You are a code debugging assistant. Just give the debugged code. No need to explain your code! Here is the code: def sum_of_squares(n):\n    total = 0\n    for i in range(1, n+1):\n        total += i ** 2\n    return total"
	}
]

stream = client.chat.completions.create(
    model="microsoft/Phi-3-mini-128k-instruct", 
    #model="meta-llama/Llama-3.2-3B-Instruct",
	messages=messages, 
	max_tokens=500,
	stream=True
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="")
