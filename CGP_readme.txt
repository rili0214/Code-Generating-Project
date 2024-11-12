Here is the structure of current generation backend:
The backend server will be deployed on an Azure VM.

├── main.py                                 # Entry point to initialize server and endpoints
├── requirements.txt                        # Dependencies for the LLMs, API interactions, and other processing
├── config.py                               # Configuration for LLM selection, API settings, and feedback loop limits
├── app/                                    # Application directory
│   ├── __init__.py                         # Initializes app as a package
│   ├── routes.py                           # API endpoints for frontend communication
│   ├── llm_manager.py                      # Core handler for LLM interactions and feedback loops
│   ├── feedback_manager.py                 # Manages the feedback loop process
│   └── utils.py                            # Utility functions for formatting, logging, etc.
├── llms/                                   # Directory for LLM handling
│   ├── base_llm.py                         # Base class for LLM interactions
│   ├── llama/                              # Subdirectory for Llama-3.1-70B-Instruct
│   │   ├── llama_generate.py               # Specific generation logic
│   │   └── llama_format_output.py          # Output formatting
│   ├── azure_openai/                       # Subdirectory for OpenAI-GPT4o-mini
│   │   ├── openai_generate.py              # Specific generation logic
│   │   └── openai_format_output.py         # Output formatting
│   ├── qwen/                               # Subdirectory for Qwen2.5-Coder-32B-Instruct
│   │   ├── qwen_generate.py                # Specific generation logic
│   │   └── qwen_format_output.py           # Output formatting
│   └── dafny_generator/                    # Directory for Dafny code generation
│       ├── dafny_generate.py               # Dafny code generation logic
├── feedback/                               # Directory for handling feedback
│   ├── __init__.py
│   └── feedback_loop.py                    # Core feedback loop logic
├── results/                                # Directory to save results
│   ├── initial_results.json                # Initial outputs from LLMs
│   ├── feedback_results.json               # Feedback results for debugging
│   └── intermediate/                       # Directory for intermediate results from each feedback loop iteration
├── logs/                                   # Directory for logging and error handling
│   ├── __init__.py
│   └── logs.txt                            # Log file
├── tests/                                  # Directory for tests
│   ├── __init__.py
│   └── test_cases.py                       # Unit and integration tests
└── temp/                                   # Temporary files directory
    └── code_files/                         # Subdirectory for temporary code files