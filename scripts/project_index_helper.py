#!/usr/bin/env python3
"""
PROJECT_INDEX Helper Script
Handles the /index command for Claude Code
"""

import sys
import subprocess
from pathlib import Path
import os

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    # Set console code page to UTF-8 on Windows
    os.system('chcp 65001 > nul 2>&1')
    # Configure Python's stdout
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    """Execute the project_index.py script"""
    # Find the scripts directory
    script_dir = Path(__file__).parent
    index_script = script_dir / 'project_index.py'
    
    # Get the saved Python command
    python_cmd_file = script_dir.parent / '.python_cmd'
    
    if python_cmd_file.exists():
        with open(python_cmd_file, 'r', encoding='utf-8') as f:
            python_cmd = f.read().strip()
    else:
        # Fallback to current Python
        python_cmd = sys.executable
    
    # Check if index script exists
    if not index_script.exists():
        print(f"[ERROR] {index_script} not found")
        print("Please ensure PROJECT_INDEX is properly installed")
        sys.exit(1)
    
    # Run the indexer with any passed arguments
    # Use encoding='utf-8' and errors='replace' to handle any encoding issues
    try:
        # Set environment variable to ensure UTF-8 encoding
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            [python_cmd, str(index_script)] + sys.argv[1:],
            check=False,
            env=env,
            encoding='utf-8',
            errors='replace',
            text=True
        )
        sys.exit(result.returncode)
    except Exception as e:
        print(f"[ERROR] Error running indexer: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()