Title: 
Code Generating Project -- Backend Server 1

Note: 
The backend server was deployed on an Azure VM, but it runs too slow, I am running it on my local repo.

Link to the overall backends workflow pipeline:
https://docs.google.com/drawings/d/1_L3x8BSyXFxRXm1XaalxutYp5_VynZwe3JpWyMylrLg/edit?usp=sharing

Structure: 
Here is the structure of current evaluation backend 1:

├── main.py                                 # Entry point to initialize server and endpoints
├── requirements.txt                        # Dependencies for the LLMs, API interactions, and other processing                 (Not yet avalibale)
├── config.py                               # Configuration for LLM selection, API settings, and feedback loop limits           (Not yet avalibale)
├── app/                                    # Application directory
│   ├── __init__.py                         # Initializes app as a package
│   ├── routes.py                           # API endpoints for frontend and the other backend server communication
│   ├── llm_manager.py                      # Core handler for LLM interactions and feedback loops
│   ├── parse_json.py                       # Helper module to save and load JSON files
│   └── utils.py                            # Utility functions for formatting
├── LLMs/                                   # Directory for LLM handling
│   ├── base_llm.py                         # Base class for LLM interactions including prompts and helper functions
│   ├── llama/                              # Subdirectory for Llama-3.2-3B-Instruct
│   │   ├── llama_generate.py               # Driver for llama model generation
│   ├── phi/                                # Subdirectory for Phi-3-mini-128k-instruct
│   │   ├── phi_generate.py                 # Driver for phi model generation
│   ├── qwen/                               # Subdirectory for Qwen2.5-Coder-32B-Instruct
│   │   ├── qwen_generate.py                # Initial, feedback, and final generation 
│   └── dafny_generator/                    # Directory for Dafny code generation using Qwen2.5-Coder-32B-Instruct
│   │   ├── dafny_generate.py               # Generation of Dafny code using Qwen model
│   └── tags_generator/                     # Directory for bug type generation using Qwen2.5-Coder-32B-Instruct
│       ├── tags_generate.py                # Generation of bug types using Qwen model to insert into the database
├── results/                                # Directory to save results
│   └── intermediate/                       # Directory for intermediate results from each feedback loop iteration
│   │   ├── phi_analysis.json               # Analysis report on Phi's code from checking phase
│   │   ├── qwen_analysis.json              # Analysis report on Qwen's code from checking phase
│   │   ├── llama_analysis,json             # Analysis report on LLaMa's code from checking phase
│   │   ├── combined_analysis.json          # Combined analysis report based on mode
│   └── phi_results                         
│   │   ├── phi_initial_results.json        # Initial generated outputs from Phi
│   └── llama_results
│   │   ├── llama_initial_results.json      # Initial generated outputs from LLaMa
│   └── qwen_results
│   │   ├── qwen_initial_results.json       # Initial generated outputs from Qwen
│   │   ├── qwen_feedback_results.json      # Feedback generated outputs from Qwen
│   └── final_analysis.json                 # Final analysis report of the feedback output
│   └── final_report.json                   # Final report including evaluation, pros&cons of code, and tips for improvements
├── database/                               # Directory to connect and operate the database
│   └── queries.py                          # Helper files that operates the database
│   └── bug_types.py                        # A json format data structure that contains most common 20 bugs for user's information
├── logs/                                   # Directory for logging and error handling
│   ├── __init__.py                         
│   └── logs.txt                            # Log file for global execution
│   └── app.logging                         # Log file for local execution
├── tests/                                  # Directory for tests
│   ├── __init__.py                         # Driver for testing
│   └── test_app_LLMs.py                    # Unit and integration tests for app and LLMs
│   └── test_database.py                    # Unit and integration tests for database
└── temp/                                   # Temporary files directory
    └── code_files/                         # Subdirectory for temporary code files