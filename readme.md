# Hephaesta 🪼

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the App](#running-the-app)
  - [Providing Inputs](#providing-inputs)
- [File Structure](#file-structure)
- [Key Components](#key-components)
- [Contributing](#contributing)
- [Known Issues](#known-issues)
- [License](#license)
- [Contact](#contact)

## Overview
Hephaesta is a web-based application built using Streamlit. It enables developers to analyze their GitHub repositories for insights into their codebase. The app helps improve coding practices and provides contextual assistance for various tasks, such as writing web crawlers and optimizing code performance. Additionally, it includes visual representations of the codebase and features an advanced problem-solving mode called "Boost".

## Features
- **Read and Analyze GitHub Repos**: Input your GitHub repository link, and the app will analyze the codebase.
- **Contextual Understanding**: Enhances user prompts with contextual information from the provided repository.
- **Boost Mode**: Offers advanced problem-solving capabilities for tackling complex problems more effectively.
- **Visual Representation**: Presents graphical visualizations of the codebase for better comprehension.

## Example uses
- **"Create a comprehensive readme"** (That's how most of this readme was created)
- **"Fix all my dependencies "**
- **"Add an input field for a private repo key, and amend the backend where needed"** (Much of this app was built by itself)
- **"Find vulnerabilities in my codebase"**
- **"List functions that aren't in use and can be deleted"**
- **"Make my code run 3x faster. Only touch the biggest time-wasters"**
- **"This repo has horrible documentation. Explain in 3 sentences."**
- **"This repo has horrible documentation. Walk me through running it."**


## Installation

### Prerequisites
- Python 3.8 or higher
- System dependencies (e.g., pip, virtualenv)

### Steps
1. Clone the repository:

    ```bash
    git clone https://github.com/Alexander5F/hephaesta    

    gitlink
    cd repo-analyzer
    ```

2. Set up the environment:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:

    - Create a `.env` file in the root directory.
    - Add your environment variables:

      ```
      VARIABLE_NAME=value
      ```

## Usage

### Running the App
Launch the Streamlit app:

```bash
streamlit run streamlit_app.py


Providing Inputs
Access the Web Interface: Open your browser and go to http://localhost:8501.
Provide GitHub URL: Input the URL of your GitHub repository.
Prompt: Input specific tasks or questions, e.g., "Optimize function X" or "Identify security vulnerabilities".
Boost Mode: Toggle the switch for enhanced problem-solving capabilities.

# File Structure

repo-analyzer/
├── streamlit_app.py                # Main Streamlit application
├── repo_visualizer.py              # Visualization logic for the codebase
├── stream_response.py              # Manages streaming responses
├── load_custom_html.py             # Loads custom HTML settings for Streamlit
├── gpt_response.py                 # Handles GPT-based responses
├── create_prompt_from_settings.py  # Generates prompts from user settings
├── render_message.py               # Renders messages in the Streamlit interface
├── handle_streamed_input.py        # Manages streamed input from users
├── check_and_delete_file_on_first_load.py  # Verifies and deletes files on first load
├── analyze_repo.py                 # Analyzes the repo and creates JSON interactions
├── module_for_main.py              # Initial setup and configurations
├── add_context_to_user_prompt.py   # Adds repo context to user prompts
├── requirements.txt                # Dependency requirements
└── .env                            # Environment variables


Key Components
streamlit_app.py: Main entry point for the Streamlit application.
repo_visualizer.py: Logic for creating visual representations of the codebase.
stream_response.py: Manages how responses are streamed in the app.
analyze_repo.py: Hosts the critical functions for analyzing the GitHub repo and transforming the data.
module_for_main.py: Handles initial setup, configurations, and logging.
add_context_to_user_prompt.py: Augments user prompts with repo context.
Contributing
Fork the repository.

Create a new branch:

bash
Copy code
git checkout -b feature-name
Commit your changes:

bash
Copy code
git commit -m "Add some feature"
Push to the branch:

bash
Copy code
git push origin feature-name
Create a Pull Request.

Please follow the coding standards and write tests for new functionalities. Refer to our Contributing Guidelines for more information.

Known Issues
Compatibility issues with Python versions below 3.8.

## Potential names
jellyfish.io
solveth.at
fixth.at
codesplo.de
