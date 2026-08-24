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

search_tool = {
    "type": "function",
    "function": {
        "name": "search",
        "description": """
            Search the internet for information.
            Use this tool whenever the user asks for:
            - current information
            - recent information
            - latest information
            - upcoming events
            - historical facts that need verification
            - information that may have changed

            After receiving search results:
            1. Read the titles and snippets.
            2. Identify which results directly answer the question.
            3. Prefer authoritative and reputable sources.
            4. Ignore irrelevant results.
            5. If the results are insufficient or contradictory, search again
            using a more specific query.
            6. Never claim something is true if the search results do not
            provide sufficient evidence.
        """,
        "parameters":{
            "type": "object",
            "properties": {
                "query":{
                    "type": "string",
                    "description": "The query that needs to be search on internet"
                }
            }
        }
    }
}

save_memory_tool = {
    "type": "function",
    "function": {
        "name": "save_memory",
        "description": (
            "Save important concepts, technical details, decisions, or contextual "
            "information from the conversation that should be referenced in future sessions."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The specific technical detail, concept, decision, or conversation point to remember."
                },
                "memory_type": {
                    "type": "string",
                    "enum": [
                        "technical_detail",
                        "project_requirement",
                        "decision_made",
                        "topic_discussed",
                        "action_item",
                        "general_knowledge"
                    ],
                    "description": "The category classification for this conversation detail."
                }
            },
            "required": [
                "content",
                "memory_type"
            ]
        }
    }
}
retrieve_memory_tool = {
    "type": "function",
    "function": {
        "name": "retrieve_memory",
        "description": (
            "Retrieves relevant information about the user "
            "that users ask and we have alsready stored our memory"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The information user asks for."
                }
            },
            "required": [
                "query"
            ]
        }
    }
}

save_user_details = {
    "type": "function",
    "function": {
        "name": "save_user_details",
        "description": (
            "Save structured information about the user. "
            "The assistant should use this tool when the user provides "
            "personal details such as name, job, education, skills, goals, "
            "preferences, hobbies, interests, projects, or other persistent facts."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "array",
                    "description": "List of structured user details.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "memory_type": {
                                "type": "string",
                                "enum": [
                                    "identity",
                                    "education",
                                    "job",
                                    "preference",
                                    "goal",
                                    "skill",
                                    "project",
                                    "interest",
                                    "hobby",
                                    "memories",
                                    "food",
                                    "fact"
                                ],
                                "description": "Category of the user detail."
                            },
                            "details": {
                                "type": "object",
                                "description": (
                                    "The actual user information as key-value pairs."
                                ),
                                "additionalProperties": True
                            }
                        },
                        "required": [
                            "memory_type",
                            "details"
                        ],
                        "additionalProperties": False
                    }
                }
            },
            "required": [
                "content"
            ],
            "additionalProperties": False
        }
    }
}

retrieve_user_details_tool = {
    "type": "function",
    "function": {
        "name": "retrieve_user_details",
        "description": (
            "Retrieve structured information about the user from long-term "
            "user memory. Use this when the user asks about their personal "
            "details such as name, job, education, skills, goals, preferences, "
            "projects, interests, hobbies, or other stored user information."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "memory_type": {
                    "type": "string",
                    "enum": [
                        "identity",
                        "education",
                        "job",
                        "preference",
                        "goal",
                        "skill",
                        "project",
                        "interest",
                        "hobby",
                        "memories",
                        "food",
                        "fact"
                    ],
                    "description": (
                        "The category of user information to retrieve. "
                        "For example, use 'identity' for name and 'job' "
                        "for the user's employment information."
                    )
                },
                "top_k": {
                    "type": "integer",
                    "description": "Maximum number of matching user details to return.",
                    "default": 3,
                    "minimum": 1,
                    "maximum": 10
                }
            },
            "required": [
                "memory_type"
            ],
            "additionalProperties": False
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
    delete_file_tool,
    search_tool,
    save_memory_tool,
    retrieve_memory_tool,
    save_user_details,
    retrieve_user_details_tool
]