# generator.py
import logging
import openai
from logs import setup_logger

# Logging Configuration
logger = setup_logger()

# Azure OpenAI API setup
AZURE_OPENAI_API_KEY = "your_azure_openai_api_key"
AZURE_OPENAI_ENDPOINT = "your_azure_openai_endpoint"

openai.api_key = AZURE_OPENAI_API_KEY
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_type = "azure"
openai.api_version = "2023-06-01-preview"  # Check Azure's latest API version

def azure_openai_generate_code(code_input, system_prompt=None, user_prompt=None):
    """Generate code using Azure's OpenAI GPT model."""
    try:
        prompt_parts = []
        if system_prompt:
            prompt_parts.append(f"System: {system_prompt}")
        if user_prompt:
            prompt_parts.append(f"User: {user_prompt}")
        prompt_parts.append(f"Code Input:\n{code_input}")
        full_prompt = "\n\n".join(prompt_parts)

        # Call Azure OpenAI API
        response = openai.Completion.create(
            engine="gpt-4",  # Replace with your deployed Azure model name, e.g., "gpt-4"
            prompt=full_prompt,
            max_tokens=300,
            temperature=0.7
        )
        generated_text = response.choices[0].text.strip()
        logger.info("Generated code with Azure OpenAI GPT model successfully.")
        return generated_text
    except Exception as e:
        logger.error(f"Error during Azure OpenAI code generation: {e}")
        raise