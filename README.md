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
