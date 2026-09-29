# MCP TempFolderManager

A secure, context-aware file management server built with Python and the Model Context Protocol (FastMCP). This tool exposes local file operations to AI agents while strictly preventing unauthorized file system access.

## Security & Path Resolution

To prevent malicious or hallucinated directory traversal by AI agents, this server employs a strict sandboxing mechanism. 

* All file operations are isolated to a dynamically created `./temp` base directory.
* A custom `get_safe_path` function resolves all incoming paths (including relative paths like `../`) to their absolute paths.
* The server explicitly verifies that the resolved target path begins with the base directory path. 
* If an agent attempts to access or modify files outside the designated sandbox, the server denies access and raises a `ValueError`.

## Features (Agent Tools)

The server exposes five callable tools for AI agents:

* **`list_files`**: Lists all files currently residing in the temp folder.
* **`create_file`**: Creates a new file or overwrites an existing one with provided string content.
* **`read_file`**: Reads and returns the text contents of a specified file.
* **`delete_file`**: Safely unlinks and removes a file from the sandbox.
* **`move_file`**: Moves or renames a file from a source path to a destination path within the sandbox.

## Installation & Setup

1. Ensure you have Python installed on your system.
2. Install the required MCP library:
   ```bash
   pip install mcp
   ```
3. Run the server:
   ```bash
   python main.py
   ```

## Usage

The server is configured to run using Standard I/O (`mcp.run()`). 
This allows any standard MCP client to connect, discover the schema, and autonomously invoke the file management tools within the secure sandbox context.
