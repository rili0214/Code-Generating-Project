# llms/qwen2_5_72b_instruct/generate.py
import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from pathlib import Path

# Set up logging
log_file_path = Path(__file__).parent.parent.parent / 'logs' / 'logs.txt'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load model and tokenizer from Hugging Face
model_name = "Qwen/Qwen2.5-72B-Instruct"
try:
    logger.info(f"Loading model '{model_name}'...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    logger.info(f"Model '{model_name}' loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model or tokenizer: {e}")
    raise

# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Using device: {device}")
model = model.to(device)

# Set up text generation pipeline
try:
    text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if device == "cuda" else -1)
    logger.info("Text generation pipeline created successfully.")
except Exception as e:
    logger.error(f"Failed to create text generation pipeline: {e}")
    raise

def generate_code(code_input, system_prompt=None, user_prompt=None):
    """Generate code using the specified LLM model on GPU with system and user prompts."""
    try:
        prompt_parts = []
        
        if system_prompt:
            prompt_parts.append(f"System: {system_prompt}")
        if user_prompt:
            prompt_parts.append(f"User: {user_prompt}")
        
        # Append code input after user prompt
        prompt_parts.append(f"Code Input:\n{code_input}")

        # Create the final prompt
        full_prompt = "\n\n".join(prompt_parts)
        
        # Log prompt preview
        logger.info(f"Generating code with full prompt:\n{full_prompt[:50]}...")

        # Generate text with the model
        generation_output = text_generator(full_prompt, max_length=300, num_return_sequences=1, temperature=0.7)
        result = generation_output[0]['generated_text']
        logger.info("Generated LLaMa code successfully.")
        return result
    except Exception as e:
        logger.error(f"Error during code generation: {e}")
        raise

if __name__ == "__main__":
    # Example usage with system and user prompts
    code_input = "def add(a, b):\n    return a + b\n\nresult = add(3, 4)\nprint(result)"
    system_prompt = "You are a coding assistant specialized in debugging."
    user_prompt = "Please help debug and improve the following code."
    generated_code = generate_code(code_input, system_prompt=system_prompt, user_prompt=user_prompt)
    print("Generated Code:", generated_code)
