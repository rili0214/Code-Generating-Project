from huggingface_hub import InferenceClient
from pathlib import Path
from LLMs.base_llm import API_TOKEN_llama, system_prompt, user_prompt, prepare_messages, call_huggingface_chat, save_response_to_json
from logs import setup_logger

llama_initial_path = str(Path(__file__).parent.parent / 'results' / 'llama_results' / 'llama_initial_results.json')

# Logging Configuration
logger = setup_logger()

# Configuration Constants
client = InferenceClient(api_key = API_TOKEN_llama)

model = "meta-llama/Llama-3.2-3B-Instruct"

def initial_call(mode, code_, language):
    system_prompt_ = system_prompt
    user_prompt_ = user_prompt
    code_input_ = code_

    messages = prepare_messages(system_prompt_, user_prompt_, code_snippet = code_input_)
    logger.info("LLaMa execution started.")

    response = call_huggingface_chat(model, messages)
    logger.info("LLaMa execution completed.")
    
    if response:
        save_response_to_json(mode=mode, model="llama", generated_code=response, call_type="llama_initial", language=language)
        logger.info("Generated LLaMa output saved to " + llama_initial_path)
    else:
        logger.error("Failed to generate LLaMa output.")


if __name__ == "__main__":
    code = "def twosum(nums, target):\n    nums.sort()\n    for i in range(len(nums)):\n        for j in range(i + 1, len(nums)):\nif nums[i] + nums[j] == target:\n                return [j, i]\n    return []"
    initial_call(mode="mode_1", code_=code, language="Python")