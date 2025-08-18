# CLAUDE-CODE-PROJECT-INDEX (Windows)

**Windows-optimized version** of the Project Index tool for Claude Code. Creates comprehensive architectural awareness of your codebase through static analysis and pattern recognition.

> **Based on the original [claude-code-project-index](https://github.com/ericbuess/claude-code-project-index) by [Eric Buess](https://github.com/ericbuess)**
> 
> This Windows-specific fork provides full compatibility with Windows systems, addressing encoding issues and path handling that affect the original cross-platform version.

## 🚀 Quick Install

```cmd
# Clone this repository
git clone https://github.com/dusancv22/CLAUDE-CODE-PROJECT-INDEX-WIN.git
cd CLAUDE-CODE-PROJECT-INDEX-WIN

# Run the installer
python install.py
```

That's it! The tool is installed with automatic hooks for maintaining the index.

## 📖 Usage

### Create an Index for Your Project

Navigate to any project directory in Claude Code and run:
```
/index
```

Or from command line:
```cmd
py "%USERPROFILE%\.claude-code-project-index\scripts\project_index.py"
```

This creates `PROJECT_INDEX.json` with:
- Complete function/class signatures
- Call graphs showing what calls what
- Directory structure and purposes
- Import dependencies
- Documentation structure

### Using the Index

Reference it when you need architectural awareness:
```
@PROJECT_INDEX.json what functions call authenticate_user?
```

Or auto-load in every session by adding to your project's CLAUDE.md:
```markdown
@PROJECT_INDEX.json
```

## ✨ Key Features

### 🏗️ Architectural Awareness
- **Function & Class Signatures** - Full signatures with type hints
- **Call Graph Analysis** - See what calls what and what's called by what
- **Dead Code Detection** - Identify unused functions
- **Directory Purpose Inference** - Understands project structure

### 📚 Language Support
**Fully Parsed:**
- Python (.py) - Functions, classes, methods, decorators
- JavaScript/TypeScript (.js, .ts, .tsx, .jsx) - Functions, classes, imports
- Shell Scripts (.sh, .bash) - Functions, exports

**File Tracking:**
- All other common languages are tracked but not parsed for signatures

### 🔄 Automatic Updates
- **PostToolUse Hook** - Updates index when files are edited
- **Stop Hook** - Checks for staleness and external changes
- **Smart Maintenance** - Index updates itself automatically

## 🔧 Requirements

- Windows 10 or later
- Python 3.8 or higher
- Claude Code with hooks support

## 📦 Installation Details

The installer (`install.py`) will:
1. Install PROJECT_INDEX to `%USERPROFILE%\.claude-code-project-index\`
2. Create the `/index` command in Claude Code
3. Configure hooks for automatic index updates
4. Test the installation

## 🧪 Testing

Run the test suite to verify everything works:
```cmd
python test_windows.py
```

You should see:
```
[SUCCESS] All tests passed! Windows compatibility confirmed.
```

## 🗑️ Uninstalling

To completely remove PROJECT_INDEX:
```cmd
python uninstall.py
```

This removes the installation directory, hooks, and commands. Your PROJECT_INDEX.json files in projects remain untouched.

## 💡 How It Works

1. **One-Time Setup Per Project** - Run `/index` once in any project
2. **Automatic Updates** - Hooks update the index on every file change
3. **External Change Detection** - Detects when files change outside Claude
4. **Smart Reindexing** - Triggers full reindex when structure changes

## 🛠️ Windows-Specific Optimizations

This version includes several Windows-specific improvements:

- **ASCII-Only Output** - No Unicode encoding errors in Windows console
- **Proper Path Handling** - Correctly handles Windows paths with spaces
- **Direct Python Execution** - No shell script dependencies
- **UTF-8 Configuration** - Proper encoding setup for Windows

## 📊 What Gets Indexed

The tool creates a comprehensive map of your project:

```json
{
  "project_structure": {
    "tree": ["Directory structure visualization"]
  },
  "files": {
    "path/to/file.py": {
      "functions": {"function_name": {"signature": "...", "calls": [...], "called_by": [...]}},
      "classes": {"ClassName": {"methods": {...}, "inherits": [...]}}
    }
  },
  "dependency_graph": {"file": ["imports"]},
  "documentation_map": {"README.md": {"sections": [...]}}
}
```

## 🎯 Benefits for Claude Code

- **Prevents code duplication** - Claude sees all existing functions
- **Ensures proper file placement** - Directory purposes guide location
- **Maintains consistency** - Follows existing patterns
- **Complete context** - Full architectural awareness
- **Faster development** - No time wasted searching

## 📝 Configuration

### Ignored Directories
Edit `IGNORE_DIRS` in `scripts/index_utils.py` to customize which directories are excluded.

### Size Limits
- MAX_FILES = 10000 (in project_index.py)
- MAX_INDEX_SIZE = 1MB (triggers compression)
- MAX_TREE_DEPTH = 5 (directory tree depth)

## 🤝 Contributing

Issues and pull requests are welcome! This is a Windows-specific fork optimized for Windows users.

## 📜 License

MIT License - See LICENSE file

## 🙏 Credits

- **Original Project**: [claude-code-project-index](https://github.com/ericbuess/claude-code-project-index) by [Eric Buess](https://github.com/ericbuess)
- **Windows Version**: Optimized for Windows by Dusan Cvjetkovic

## 📚 Related Projects

- **Original Cross-Platform Version**: [claude-code-project-index](https://github.com/ericbuess/claude-code-project-index) - For macOS/Linux support
- **Claude Code Docs**: [claude-code-docs](https://github.com/ericbuess/claude-code-docs) - Companion documentation tool