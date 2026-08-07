calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Perform mathematical operations on two numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The mathematical operation to perform."
                },
                "a": {
                    "type": "number",
                    "description": "First number."
                },
                "b": {
                    "type": "number",
                    "description": "Second number."
                }
            },
            "required": ["operation", "a", "b"]
        }
    }
}

current_time_tool = {
    "type": "function",
    "function": {
        "name": "current_time",
        "description": "Returns the current date and time for a given timezone.",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "Timezone in IANA format, e.g. Asia/Kolkata, Asia/Tokyo, America/New_York."
                }
            },
            "required": ["timezone"]
        }
    }
}

current_date_tool = {
    "type": "function",
    "function": {
        "name": "current_date",
        "description": "Returns the current date in YYYY-MM-DD format.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}

weather_tool = {
    "type": "function",
    "function": {
        "name": "weather",
        "description": "Returns the current weather for a given latitude and longitude.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "number",
                    "description": "Latitude of the location."
                },
                "longitude": {
                    "type": "number",
                    "description": "Longitude of the location."
                }
            },
            "required": ["latitude", "longitude"]
        }
    }
}

geocoder_tool = {
    "type":"function",
    "function": {
        "name": "geocoder",
        "description": "Returns the latitude and longitude for a given address.",
        "parameters": {
            "type": "object",
            "properties": {
                "address": {
                    "type": "string",
                    "description": "The address to geocode."
                }
            },
            "required": ["address"]
        }
    }
}

read_file_tool = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Reads the content of a text file and returns it as a string.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the text file."
                }
            },
            "required": ["file_path"]
        }
    }
}

write_file_tool = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes a string to a text file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the text file."
                },
                "text": {
                    "type": "string",
                    "description": "The text content to write to the file."
                }
            },
            "required": ["file_path", "text"]
        }
    }
}

list_files_tool = {
    "type": "function",
    "function": {
        "name": "list_files_in_directory",
        "description": "List all files inside a directory. "
            "Use this tool whenever the user asks to list files, show files, "
            "display files, or see the contents of a folder.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory_path": {
                    "type": "string",
                    "description": "The path to the directory."
                }
            },
            "required": ["directory_path"]
        }
    }
}

delete_file_tool = {
    "type": "function",
    "function": {
        "name": "delete_file",
        "description": "Deletes a file at the specified path.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to delete."
                }
            },
            "required": ["file_path"]
        }
    }
}

tools = [
    calculator_tool,
    current_time_tool,
    current_date_tool,
    weather_tool,
    geocoder_tool,
    read_file_tool,
    write_file_tool,
    list_files_tool,
    delete_file_tool
]