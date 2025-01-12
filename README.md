# Setting Up a Python Virtual Environment

Follow these steps to set up a Python virtual environment:

1. **Create a virtual environment:**
    ```sh
    python3 -m venv .venv
    ```

2. **Activate the virtual environment:**

    - On macOS and Linux:
        ```sh
        source .venv/bin/activate
        ```
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```

3. **Upgrade `pip`:**
    ```sh
    pip install --upgrade pip
    ```

4. **Intall requirements:**
    ```sh
    pip install -r requirements.txt
    ```

5.  **Install Ollama:**

Download and install Ollama from GitHub to run Llama models locally

6. **Pull Necessary Model:**

Once Ollama is installed, pull the necessary model (Llama 3.2 3B):
    ```sh
    ollama pull llama3.2
    ```
Note: you will find model blod in ~/.ollama/models