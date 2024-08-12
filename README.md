
# LLM Dataset Builder Flask App

## Overview

This Flask application provides an interface for formatting conversation data for use with the OpenAI API's fine-tuning for chat models. The app allows users to input a system prompt, multiple user prompts, and assistant responses. The data is formatted into the required JSON structure and can be downloaded as a `.jsonl` file directly from the browser. This application is designed to help prepare datasets for fine-tuning language models with structured conversations.

## Features

- **Dynamic Form**: Add and remove user-assistant turns dynamically.
- **JSON Formatting**: The input data is formatted into the required JSON structure with an optional assistant message weight.
- **Downloadable Output**: The formatted conversations can be downloaded as a `.jsonl` file directly from the browser.
- **Browser-side Data Handling**: The dataset is stored in the user's client until the download button is pressed.

## Requirements

To run this application, you need the following:

- **Python 3.7+**
- **Flask** (Python web framework)
- **A modern web browser**

### Python Dependencies

The required Python packages can be installed using `pip`. The dependencies include:

- Flask

Install the dependencies by running:

```bash
pip install Flask
```

## Directory Structure

The directory structure for this application:

```
llm-dataset-builder/
│
├── app.py                  # Main Flask application script
├── static/
│   └── script.js           # JavaScript file for dynamic form interactions
└── templates/
    └── index.html          # HTML template for the app's interface
```

- **app.py**: The main application script containing the Flask routes and logic.
- **static/script.js**: The JavaScript file that handles dynamic form interactions.
- **templates/index.html**: The HTML template for the web interface.

## Running the Application

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Make-A-Face-Publishing/llm-dataset-builder.git
   cd llm-dataset-builder
   ```

2. **Install Flask**:
   ```bash
   pip install Flask
   ```

3. **Run the Flask Application**:
   ```bash
   flask run
   ```
   OR
   ```bash
   python app.py
   ```   
4. **Access the App**:
   Open your web browser and navigate to `http://127.0.0.1:5000/` to use the application.

## Notes

- The `/save` route is included for those who wish to save formatted entries on the server-side. This feature is not currently integrated into the UI but is available for extending the app's functionality.
