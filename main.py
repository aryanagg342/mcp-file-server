from mcp.server.fastmcp import FastMCP
import os
import shutil
from pathlib import Path

mcp = FastMCP("TempFolderManager")

BASE_DIR = Path("./temp").resolve()
BASE_DIR.mkdir(exist_ok=True)

def get_safe_path(filename: str) -> Path:
    """Security helper: Ensures the path stays strictly within the temp directory."""
    # Resolve resolves relative paths like '../' to absolute paths
    target_path = (BASE_DIR / filename).resolve()
    
    # Check if the resolved path still starts with the base directory path
    if not str(target_path).startswith(str(BASE_DIR)):
        raise ValueError(f"Access denied: '{filename}' attempts to access outside the temp folder.")
    return target_path

@mcp.tool()
def list_files() -> str:
    """List all files currently in the temp folder."""
    files = os.listdir(BASE_DIR)
    if not files:
        return "The temp folder is empty."
    return f"Files in temp: {', '.join(files)}"

@mcp.tool()
def create_file(filename: str, content: str) -> str:
    """Create a new file (or overwrite an existing one) in the temp folder."""
    safe_path = get_safe_path(filename)
    safe_path.write_text(content)
    return f"Successfully created/updated {filename}."

@mcp.tool()
def read_file(filename: str) -> str:
    """Read the contents of a file in the temp folder."""
    safe_path = get_safe_path(filename)
    if not safe_path.exists():
        return f"Error: {filename} does not exist."
    return safe_path.read_text()

@mcp.tool()
def delete_file(filename: str) -> str:
    """Delete a file from the temp folder."""
    safe_path = get_safe_path(filename)
    if not safe_path.exists():
        return f"Error: {filename} does not exist."
    safe_path.unlink()
    return f"Successfully deleted {filename}."

@mcp.tool()
def move_file(source: str, destination: str) -> str:
    """Move or rename a file within the temp folder."""
    src_path = get_safe_path(source)
    dest_path = get_safe_path(destination)
    
    if not src_path.exists():
        return f"Error: Source file {source} does not exist."
    
    shutil.move(src_path, dest_path)
    return f"Successfully moved {source} to {destination}."

if __name__ == "__main__":
    # Runs the server using Standard I/O (the standard way MCP clients communicate)
    mcp.run()