# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CLAUDE-CODE-PROJECT-INDEX (Windows) - A Windows-optimized code intelligence system that provides Claude Code with comprehensive architectural awareness of codebases through static analysis and pattern recognition.

## Commands

### Development and Testing
```cmd
# Test the indexer locally (from project root)
python scripts\project_index.py

# Run with version check
python scripts\project_index.py --version

# Test update hooks
python scripts\update_index.py

# Test reindex logic
python scripts\reindex_if_needed.py

# Test Windows compatibility
python test_windows.py

# Run installation
python install.py

# Uninstall the tool
python uninstall.py
```

### Installation Testing
```cmd
# Install from local repository
cd C:\Users\you\source\repos\CLAUDE-CODE-PROJECT-INDEX-WIN
python install.py

# Force reinstall without prompting
python install.py --force

# Uninstall
python uninstall.py
```

## Architecture

### Core Components

**scripts/project_index.py**
- Main indexer that creates PROJECT_INDEX.json
- Orchestrates directory traversal, file parsing, and index generation
- Handles compression when index exceeds size limits
- Entry point for `/index` command

**scripts/index_utils.py**
- Core parsing engine for extracting code signatures
- Language parsers for Python, JavaScript/TypeScript, and Shell
- Gitignore pattern matching and file filtering
- Directory purpose inference logic
- Call graph analysis functions

**scripts/update_index.py**
- PostToolUse hook handler for incremental updates
- Updates index when files are edited through Claude
- Maintains index freshness during active sessions

**scripts/reindex_if_needed.py**
- Stop hook handler for staleness checks
- Detects external changes and structural modifications
- Triggers full reindex when necessary
- Validates index features and completeness

**scripts/detect_external_changes.py**
- Monitors for file changes outside Claude sessions
- Checks git status for uncommitted changes
- Used by reindex_if_needed.py

**scripts/project_index_helper.py**
- Python helper for /index command
- Handles encoding issues for Windows console
- Executes project_index.py with proper environment

### Language Support

**Fully Parsed Languages:**
- Python (.py) - Full signatures, classes, call graphs
- JavaScript/TypeScript (.js, .ts, .tsx, .jsx) - Functions, classes, imports
- Shell Scripts (.sh, .bash) - Function signatures, exports

**Tracked Only:**
- All other common languages are listed but not parsed for signatures

### Hook Integration

The tool uses Claude Code's hook system:
- **PostToolUse Hook**: Triggers on Write|Edit|MultiEdit to update index
- **Stop Hook**: Runs staleness checks when Claude stops
- Hooks are configured in %USERPROFILE%\.claude\settings.json

## Key Design Principles

1. **Explicit Creation**: Users decide which projects need indexing via `/index`
2. **Automatic Maintenance**: Once created, indexes self-maintain
3. **Gitignore Respect**: Honors .gitignore patterns plus sensible defaults
4. **Size Management**: Automatically compresses large indexes
5. **Language Agnostic**: Extensible parser system for adding languages
6. **Windows Optimized**: ASCII-only output, proper path handling, UTF-8 configuration

## File Structure

```
CLAUDE-CODE-PROJECT-INDEX-WIN/
├── scripts/
│   ├── project_index.py         # Main indexer
│   ├── index_utils.py           # Parsing utilities
│   ├── update_index.py          # Incremental updater
│   ├── reindex_if_needed.py     # Staleness checker
│   ├── detect_external_changes.py  # External change detector
│   └── project_index_helper.py  # /index command helper
├── install.py                   # Windows installer
├── uninstall.py                 # Windows uninstaller
├── test_windows.py              # Windows compatibility tests
├── .claude/
│   └── settings.local.json     # Local Claude settings
├── README.md                    # Documentation
└── PROJECT_INDEX.json          # Generated index (when run)
```

## Adding Language Support

To add a new language parser:
1. Open scripts/index_utils.py
2. Add language to PARSEABLE_LANGUAGES set
3. Create extract_[language]_signatures() function
4. Update parse logic in project_index.py to call new parser
5. Test with sample code files

## Configuration

### Ignored Directories
Edit IGNORE_DIRS in scripts/index_utils.py:
```python
IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', ...}
```

### Size Limits
- MAX_FILES = 10000 (in project_index.py)
- MAX_INDEX_SIZE = 1MB (triggers compression)
- MAX_TREE_DEPTH = 5 (directory tree depth)

## Development Tips

- The tool uses the newest Python version available (3.8+ required)
- Python command is saved in %USERPROFILE%\.claude-code-project-index\.python_cmd
- Hooks timeout after 5-10 seconds to avoid blocking Claude
- Index compression removes non-parsed files first, then truncates tree
- Call graph analysis tracks both "calls" and "called_by" relationships

## Windows-Specific Features

- **ASCII-Only Output**: No Unicode encoding errors in Windows console
- **Path Handling**: Proper handling of Windows paths with spaces and backslashes
- **Direct Python Execution**: No shell script dependencies
- **UTF-8 Configuration**: Proper encoding setup throughout
- **Windows Console Compatibility**: Uses ASCII tree characters (+-- instead of ├──)