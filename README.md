# Agentic AI ChatBot

A lightweight Python-based chatbot framework that integrates with the OpenAI API and exposes a small set of tool functions for math, time, weather, geocoding, and basic file operations.

## Key Features

- Interactive CLI chat loop via `main.py`
- OpenAI function-calling support through tool definitions in `tool_schemas.py`
- Tool implementations in `tools/`
- Environment-driven configuration with `python-dotenv`
- Utility tools for:
  - arithmetic (`calculator`)
  - current date/time (`current_date`, `current_time`)
  - weather lookup (`weather`)
  - geocoding (`geocoder`)
  - file read/write/list/delete operations (`read_file`, `write_file`, `list_files_in_directory`, `delete_file`)

## Project Structure

- `main.py` - Primary interactive chat entrypoint.
- `main-1.py` - Alternate chat loop implementation.
- `config.py` - Loads OpenAI and third-party API settings from environment variables.
- `tool_schemas.py` - Defines the JSON schema for each tool exposed to the OpenAI assistant.
- `tool_registry.py` - Maps tool names to Python function implementations.
- `tools/` - Tool implementations used by the assistant.
- `requirement.txt` - Python dependencies.

## Requirements

- Python 3.11+ (for `zoneinfo` and modern package compatibility)
- `pip`
- An OpenAI-compatible API endpoint and credentials
- Optional weather/geocoder API endpoints for location-based tools

## Setup

1. Install dependencies:

```bash
pip install -r requirement.txt
```

2. Create a `.env` file in the project root with the required variables:

```env
BASE_URL=<openai_base_url>
API_KEY=<openai_api_key>
MODEL=<openai_model_name>
WEATHER_API=<weather_api_url_or_keyed_endpoint>
GEOCODER_API=<geocoder_api_url>
```

3. Verify the `.env` values are correct and accessible.

## Usage

Run the chatbot from the project root:

```bash
python main.py
```

Then type messages at the prompt. Enter `exit` to end the session.

## Available Tools

The assistant can call the following tools when the user request requires external information or actions:

- `calculator(operation, a, b)`
- `current_time(timezone)`
- `current_date()`
- `weather(latitude, longitude)`
- `geocoder(address)`
- `read_file(file_path)`
- `write_file(file_path, text)`
- `list_files_in_directory(directory_path)`
- `delete_file(file_path)`

## Notes

- `config.py` uses `python-dotenv` to load environment variables.
- The project is designed as a starting point for building an agentic chatbot with function-calling support.
- If you want to extend the assistant, add new tool schemas in `tool_schemas.py`, map them in `tool_registry.py`, and implement the tool logic in `tools/`.

## License

This repository does not include a license file. Add one if you wish to share or reuse the project publicly.
