# llms/llama_31_nemotron_70b/generate.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model and tokenizer, using a Hugging Face model from their hub
model_name = "nvidia/Llama-3.1-Nemotron-70B-Instruct" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Move model to GPU if available
if torch.cuda.is_available():
    model = model.to("cuda")

def generate_code(code_input):
    """Generate debugged code using the specified LLM model on GPU."""
    inputs = tokenizer(code_input, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
    outputs = model.generate(inputs["input_ids"], max_new_tokens=100, do_sample=True, temperature=0.7)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result

