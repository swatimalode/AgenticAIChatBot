# Agentic AI ChatBot

A lightweight Python-based Agentic AI chatbot that integrates an LLM with tool calling, streaming responses, short-term memory, long-term memory, embeddings, ChromaDB, document chunking, and Retrieval-Augmented Generation (RAG).

## Key Features

- FastAPI-based chatbot
- Streaming LLM responses
- OpenAI-compatible API support
- LLM function/tool calling
- Short-term conversation memory
- Long-term memory
- Embeddings for semantic search
- ChromaDB vector database
- Document upload and processing
- Token-based document chunking
- Retrieval-Augmented Generation (RAG)
- Semantic document search
- Multiple document support
- Persistent vector storage

## Architecture

```text
                         User
                          |
                          v
                    +-----------+
                    |    LLM    |
                    +-----+-----+
                          |
             +------------+------------+
             |            |            |
             v            v            v
       Short-Term    Long-Term      Documents
         Memory        Memory         / RAG
             |            |             |
             v            v             v
           RAM         ChromaDB      ChromaDB
                          |
                          v
                    Retrieved Data
                          |
                          v
                         LLM
                          |
                          v
                       Response
````

## Project Structure

```text
AgenticAIChatBot/
│
├── main.py
├── config.py
├── tool_schemas.py
├── tool_registry.py
├── requirement.txt
│
├── memory/
│   ├── memory_manager.py
│   └── long_term_memory.py
│
├── tools/
│   ├── calculator.py
│   ├── weather.py
│   ├── current_date.py
│   ├── current_time.py
│   ├── geocoder.py
│   └── ...
│
└── utils/
    ├── embedding.py
    ├── similarity.py
    ├── vector_db.py
    ├── chunker.py
    └── prompt.py
```

## Components

### `main.py`

Main FastAPI application responsible for:

* Receiving chat messages
* Receiving uploaded documents
* Calling the LLM
* Streaming responses
* Handling tool calls
* Managing short-term conversation memory

### `config.py`

Loads configuration from environment variables using `python-dotenv`.

### `tool_schemas.py`

Contains the JSON schemas for the tools exposed to the LLM.

### `tool_registry.py`

Maps tool names to their Python implementations.

Example:

```python
tool_registry = {
    "calculator": calculator,
    "weather": weather,
    "search_documents": search_documents,
}
```

The tool name must match the name defined in `tool_schemas.py`.

### `memory/memory_manager.py`

Manages short-term conversation memory.

Recent messages are kept in memory while older messages can be summarized to reduce the amount of conversation sent to the LLM.

### `memory/long_term_memory.py`

Manages persistent information such as:

* User details
* Long-term conversation memories
* Semantic memory retrieval
* Memory updates and deletion

Long-term conversation memories use embeddings and ChromaDB for semantic retrieval.

### `utils/embedding.py`

Generates embeddings for text.

Embeddings convert text into numerical vectors that can be compared based on semantic meaning.

For example:

```text
"What are the company holidays?"
```

can retrieve information such as:

```text
"Employees receive 24 days of annual leave."
```

even though the wording is different.

### `utils/vector_db.py`

Provides access to ChromaDB.

Different collections are used for different types of data:

```text
ChromaDB
│
├── conversation_memory
│
└── rag_documents
```

### `utils/chunker.py`

Processes uploaded documents.

The document ingestion pipeline is:

```text
Document
   |
   v
Extract Text
   |
   v
Tokenization
   |
   v
Chunking
   |
   v
Generate Embeddings
   |
   v
Store in ChromaDB
```

## Memory

The chatbot uses different types of memory for different purposes.

### Short-Term Memory

Stores recent messages from the current conversation.

```text
User message
      |
      v
Short-term memory
      |
      v
LLM context
```

Short-term memory is kept in application memory and is not intended to be permanent.

### Long-Term Memory

Stores information that should remain available for future conversations.

Examples:

* User information
* Preferences
* Important conversation information

Long-term conversation memories are stored using embeddings in ChromaDB.

## RAG

RAG (Retrieval-Augmented Generation) allows the chatbot to answer questions using information from uploaded documents.

### Document ingestion

```text
Upload document
      |
      v
Extract text
      |
      v
Split into chunks
      |
      v
Generate embeddings
      |
      v
Store chunks in ChromaDB
```

### Document retrieval

When the user asks a question:

```text
User Question
      |
      v
Generate Query Embedding
      |
      v
ChromaDB Semantic Search
      |
      v
Relevant Document Chunks
      |
      v
LLM
      |
      v
Final Answer
```

The entire document is not sent to the LLM for every question. Only relevant chunks are retrieved.

## Document IDs

Each uploaded document receives a unique `document_id`.

For example:

```text
company.txt
     |
     v
document_id = abc123
     |
     +-- abc123_0
     +-- abc123_1
     +-- abc123_2
```

Each chunk contains metadata such as:

```python
{
    "document_id": document_id,
    "chunk_index": index,
    "filename": file.filename
}
```

This allows multiple documents to be stored in the same `rag_documents` collection.

A separate ChromaDB collection is not required for every document.

## Available Tools

The chatbot can expose the following tools to the LLM.

### Calculator

```text
calculator(operation, a, b)
```

Performs arithmetic operations.

### Current Time

```text
current_time(timezone)
```

Returns the current time for a given timezone.

### Current Date

```text
current_date()
```

Returns the current date.

### Weather

```text
weather(latitude, longitude)
```

Retrieves weather information.

### Geocoder

```text
geocoder(address)
```

Converts an address into geographic coordinates.

### File Operations

```text
read_file(file_path)
write_file(file_path, text)
list_files_in_directory(directory_path)
delete_file(file_path)
```

Provides basic file-system operations.

### Document Search

```text
search_documents(query)
```

Searches uploaded documents using semantic similarity.

This tool is used when the user's question requires information from an uploaded document.

## Memory vs RAG

Memory and RAG serve different purposes.

| Component         | Purpose                                  | Storage            |
| ----------------- | ---------------------------------------- | ------------------ |
| Short-term memory | Recent conversation context              | Application memory |
| Long-term memory  | Persistent user/conversation information | JSON + ChromaDB    |
| RAG documents     | Information from uploaded documents      | ChromaDB           |
| Embeddings        | Semantic representation of text          | ChromaDB           |

In simple terms:

```text
Memory = What the chatbot remembers

RAG = Information the chatbot retrieves from documents
```

ChromaDB is the vector database used to store and search embeddings.

## Requirements

* Python 3.11+
* pip
* FastAPI
* Uvicorn
* ChromaDB
* tiktoken
* python-dotenv
* OpenAI-compatible LLM API
* Embedding model/API

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd AgenticAIChatBot
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirement.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
BASE_URL=<openai_compatible_base_url>
API_KEY=<api_key>
MODEL=<model_name>

EMBEDDING_MODEL=<embedding_model>

CHUNK_SIZE=500
OVERLAP_CHUNK_SIZE=50
```

The application uses an OpenAI-compatible API interface, so the LLM provider can be changed through configuration.

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

The application will be available at:

```text
http://localhost:8080
```

Health check:

```text
GET /health
```

Chat endpoint:

```text
POST /chat
```

## Example

Suppose the uploaded document contains:

```text
Infosys company provides 24 days of annual leave.

Employees can work remotely three days per week.

The working hours are from 9 AM to 6 PM.

Employees receive health insurance after completing three months.

The notice period for full-time employees is 60 days.
```

The user can ask:

```text
How many annual leaves are allowed?
```

The chatbot retrieves the relevant document chunk and responds:

```text
The company provides 24 days of annual leave.
```

The user can also ask:

```text
What are the working hours?
```

or:

```text
Can you summarize the document?
```

## Agentic Tool Calling

The LLM decides when a tool is required.

For example:

```text
User
 |
 | "What is 25 * 4?"
 v
LLM
 |
 | calculator(...)
 v
Tool
 |
 | 100
 v
LLM
 |
 v
"25 * 4 = 100"
```

For document-based questions:

```text
User
 |
 | "How many annual leaves are allowed?"
 v
LLM
 |
 | search_documents(...)
 v
ChromaDB
 |
 | Relevant chunks
 v
LLM
 |
 v
Final answer
```

## Design Principles

### Separate retrieval sources

The chatbot does not treat every piece of information as the same type of memory.

```text
Short-term memory
        |
        +-- Recent conversation

Long-term memory
        |
        +-- Persistent user/conversation information

RAG
        |
        +-- Uploaded document information
```

### Backend owns internal IDs

Identifiers such as:

```text
document_id
conversation_id
user_id
```

are managed by the backend.

The LLM should focus on the semantic question rather than managing internal database IDs.

### Do not store entire documents in chat memory

Uploaded documents remain in ChromaDB.

Only relevant document chunks are retrieved when needed.

### Keep tools focused

Instead of using one large retrieval tool:

```text
search_everything()
```

the chatbot uses focused tools:

```text
search_memory()
search_documents()
weather()
calculator()
```

This makes the agent easier to control and debug.

## Learning Roadmap

This project is being developed incrementally to understand the core components of Agentic AI:

```text
Python
   |
   v
LLM API
   |
   v
Prompt Engineering
   |
   v
Tool Calling
   |
   v
Streaming
   |
   v
Short-Term Memory
   |
   v
Long-Term Memory
   |
   v
Embeddings
   |
   v
Vector Database
   |
   v
Document Chunking
   |
   v
RAG
   |
   v
Agentic Retrieval
```

The goal is to understand how these components work together rather than relying entirely on an AI framework.

## License

This repository currently does not include a license file.

If you plan to distribute or reuse this project publicly, add an appropriate open-source license.

```
```
