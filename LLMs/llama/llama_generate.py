from huggingface_hub import InferenceClient
from pathlib import Path
from LLMs.base_llm import API_TOKEN_llama, system_prompt, user_prompt, prepare_messages, call_huggingface_chat, save_response_to_json
from logs import setup_logger

# Logging Configuration
logger = setup_logger()

# Configuration Constants
client = InferenceClient(api_key = API_TOKEN_llama)

model = "meta-llama/Llama-3.2-3B-Instruct"

def initial_call(code_):
    system_prompt_ = system_prompt
    user_prompt_ = user_prompt
    code_input_ = code_

    messages = prepare_messages(system_prompt_, user_prompt_, code_snippet = code_input_)
    logger.info("LLaMa execution started.")

    response = call_huggingface_chat(model, messages)

    save_response_to_json(response, "llama", "llama_initial")
    logger.info("LLaMa execution completed.")


if __name__ == "__main__":
    initial_call("def twosum(nums, target):\n    nums.sort()\n    for i in range(len(nums)):\n        for j in range(i + 1, len(nums)):\nif nums[i] + nums[j] == target:\n                return [j, i]\n    return []")