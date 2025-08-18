#!/usr/bin/env python3
"""
CLAUDE-CODE-PROJECT-INDEX (Windows) Installer
Windows-specific installer for PROJECT_INDEX tool
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
import argparse

# Set UTF-8 encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

# Version info
VERSION = "1.0.0-win"
INSTALL_DIR = Path.home() / ".claude-code-project-index"

def print_header():
    """Print installation header"""
    print("CLAUDE-CODE-PROJECT-INDEX (Windows) Installer")
    print("=" * 50)
    print()

def find_python():
    """Find the best Python interpreter to use on Windows"""
    print("\n[INFO] Detecting Python version...")
    
    # If in virtual environment, use that
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"   [OK] Using virtual environment Python: {sys.executable}")
        return sys.executable
    
    # Check for PYTHON_CMD environment variable
    if os.environ.get('PYTHON_CMD'):
        python_cmd = os.environ['PYTHON_CMD']
        try:
            version = subprocess.check_output([python_cmd, '--version'], text=True, stderr=subprocess.STDOUT)
            print(f"   [OK] Using PYTHON_CMD: {python_cmd}")
            print(f"      Version: {version.strip()}")
            return python_cmd
        except:
            print(f"   [WARNING] PYTHON_CMD={python_cmd} not valid, searching for alternatives...")
    
    # Find all Python installations on Windows
    python_commands = []
    
    # Common Python command names on Windows
    candidates = ['py', 'python', 'python3']
    
    for cmd in candidates:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                version_line = result.stdout.strip() or result.stderr.strip()
                version_parts = version_line.split()[-1].split('.')
                if len(version_parts) >= 2:
                    major = int(version_parts[0])
                    minor = int(version_parts[1])
                    if major == 3 and minor >= 8:  # Python 3.8+
                        python_commands.append((cmd, major, minor, version_line))
                        print(f"   [OK] Found {version_line} at: {cmd}")
        except (subprocess.SubprocessError, ValueError, FileNotFoundError):
            continue
    
    if not python_commands:
        print("\n[ERROR] Python 3.8+ is required but not found")
        print("\nPlease install Python 3.8 or higher:")
        print("  - Download from https://www.python.org/downloads/")
        print("  - Or install via Microsoft Store")
        print("  - Or use: winget install Python.Python.3.12")
        sys.exit(1)
    
    # Sort by version (newest first)
    python_commands.sort(key=lambda x: (x[1], x[2]), reverse=True)
    
    # Use the newest version
    best_python = python_commands[0][0]
    print(f"\n   [INFO] Selected newest version: Python {python_commands[0][1]}.{python_commands[0][2]}")
    print(f"      Using: {best_python}")
    
    return best_python

def check_dependencies():
    """Check for optional dependencies"""
    print("\nChecking dependencies...")
    
    # Git is optional
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True, timeout=2)
        print("   [OK] Git found (optional)")
        has_git = True
    except:
        print("   [INFO] Git not found (optional)")
        has_git = False
    
    print("[OK] All required dependencies satisfied")
    return has_git

def backup_settings(settings_file):
    """Create a backup of settings.json"""
    if settings_file.exists():
        backup_file = settings_file.with_suffix('.json.backup')
        shutil.copy2(settings_file, backup_file)
        return backup_file
    return None

def update_hooks(settings_file, install_dir):
    """Update hooks in settings.json for Windows"""
    print("\nConfiguring hooks...")
    
    # Ensure settings directory exists
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing settings or create new
    if settings_file.exists():
        backup_file = backup_settings(settings_file)
        if backup_file:
            print(f"   [OK] Backed up settings to {backup_file}")
        
        with open(settings_file, 'r') as f:
            settings = json.load(f)
    else:
        settings = {}
    
    # Initialize hooks structure
    if 'hooks' not in settings:
        settings['hooks'] = {}
    if 'PostToolUse' not in settings['hooks']:
        settings['hooks']['PostToolUse'] = []
    if 'Stop' not in settings['hooks']:
        settings['hooks']['Stop'] = []
    
    # Get Python command for hooks
    python_cmd_file = install_dir / '.python_cmd'
    if python_cmd_file.exists():
        with open(python_cmd_file, 'r') as f:
            python_exe = f.read().strip()
    else:
        python_exe = sys.executable
    
    # Remove old PROJECT_INDEX hooks
    settings['hooks']['PostToolUse'] = [
        hook for hook in settings['hooks']['PostToolUse']
        if not any('update_index.py' in str(h.get('command', '')) or 
                  'project_index' in str(h.get('command', ''))
                  for h in hook.get('hooks', []))
    ]
    
    settings['hooks']['Stop'] = [
        hook for hook in settings['hooks']['Stop']
        if not any('reindex_if_needed.py' in str(h.get('command', '')) or
                  'project_index' in str(h.get('command', ''))
                  for h in hook.get('hooks', []))
    ]
    
    # Add new hooks with Python direct execution (Windows paths)
    update_script = str(install_dir / 'scripts' / 'update_index.py')
    reindex_script = str(install_dir / 'scripts' / 'reindex_if_needed.py')
    
    settings['hooks']['PostToolUse'].append({
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [{
            "type": "command",
            "command": f'"{python_exe}" "{update_script}"',
            "timeout": 5
        }]
    })
    
    settings['hooks']['Stop'].append({
        "matcher": "",
        "hooks": [{
            "type": "command",
            "command": f'"{python_exe}" "{reindex_script}"',
            "timeout": 10
        }]
    })
    
    # Write updated settings
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print("[OK] Hooks configured in settings.json")

def create_index_command(python_cmd):
    """Create the /index command for Windows"""
    print("\nCreating /index command...")
    
    commands_dir = Path.home() / '.claude' / 'commands'
    commands_dir.mkdir(parents=True, exist_ok=True)
    
    index_cmd_file = commands_dir / 'index.md'
    helper_script = INSTALL_DIR / 'scripts' / 'project_index_helper.py'
    
    command_content = f'''Create or update PROJECT_INDEX.json for the current project.

Use the Bash tool to execute this command:
{python_cmd} "{helper_script}"

This analyzes your codebase and creates PROJECT_INDEX.json with:
- Directory tree structure
- Function/method signatures  
- Class inheritance relationships
- Import dependencies
- Documentation structure
- Language-specific parsing for Python, JavaScript/TypeScript, and Shell scripts

The index is automatically updated when you edit files through PostToolUse hooks.
'''
    
    with open(index_cmd_file, 'w') as f:
        f.write(command_content)
    
    print("[OK] Created /index command")

def install_from_local(source_dir, install_dir):
    """Install from local repository"""
    print("Installing from local repository...")
    
    # Create install directory
    install_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy essential files
    files_to_copy = [
        'install.py',
        'uninstall.py',
        'test_windows.py',
        'README.md',
        'LICENSE',
        '.gitignore',
        'PROJECT_INDEX.json',
        'CLAUDE.md'
    ]
    
    for file in files_to_copy:
        source_file = source_dir / file
        if source_file.exists():
            shutil.copy2(source_file, install_dir / file)
    
    # Copy scripts directory
    scripts_src = source_dir / 'scripts'
    scripts_dst = install_dir / 'scripts'
    if scripts_src.exists():
        if scripts_dst.exists():
            shutil.rmtree(scripts_dst)
        shutil.copytree(scripts_src, scripts_dst)
    
    print(f"[OK] Files copied to {install_dir}")

def test_installation(python_cmd):
    """Test the installation"""
    print("\nTesting installation...")
    
    test_script = INSTALL_DIR / 'scripts' / 'project_index.py'
    if test_script.exists():
        try:
            result = subprocess.run(
                [python_cmd, str(test_script), '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if 'PROJECT_INDEX' in result.stdout or result.returncode == 0:
                print("[OK] Installation test passed")
                return True
        except:
            pass
    
    print("[WARNING] Version check failed, but installation completed")
    print("   You can still use /index command normally")
    return False

def main():
    """Main installation process"""
    parser = argparse.ArgumentParser(description='Install CLAUDE-CODE-PROJECT-INDEX (Windows)')
    parser.add_argument('--uninstall', action='store_true', help='Uninstall PROJECT_INDEX')
    parser.add_argument('--force', action='store_true', help='Force reinstall without prompting')
    args = parser.parse_args()
    
    if args.uninstall:
        # Import and run uninstall
        uninstall_script = Path(__file__).parent / 'uninstall.py'
        if uninstall_script.exists():
            import uninstall
            uninstall.main()
        else:
            print("[ERROR] Uninstall script not found")
        return
    
    print_header()
    print("[OK] Detected Windows")
    
    # Find Python
    python_cmd = find_python()
    
    # Check dependencies
    has_git = check_dependencies()
    
    # Check if already installed
    if INSTALL_DIR.exists():
        print(f"\n[WARNING] Found existing installation at {INSTALL_DIR}")
        
        if not args.force and sys.stdin.isatty():
            response = input("Remove and reinstall? (y/N): ")
            if response.lower() != 'y':
                print("Installation cancelled")
                return
        else:
            print("Removing existing installation...")
        
        shutil.rmtree(INSTALL_DIR)
    
    # Install from current directory
    current_dir = Path(__file__).parent
    print()
    install_from_local(current_dir, INSTALL_DIR)
    
    # Save Python command for later use
    python_cmd_file = INSTALL_DIR / '.python_cmd'
    with open(python_cmd_file, 'w') as f:
        f.write(python_cmd)
    print(f"   [OK] Python command saved: {python_cmd}")
    
    # Update hooks in settings.json
    settings_file = Path.home() / '.claude' / 'settings.json'
    update_hooks(settings_file, INSTALL_DIR)
    
    # Create /index command
    create_index_command(python_cmd)
    
    # Test installation
    test_installation(python_cmd)
    
    # Print success message
    print("\n" + "=" * 50)
    print("[SUCCESS] PROJECT_INDEX installed successfully!")
    print("=" * 50)
    print(f"\n[INFO] Installation location: {INSTALL_DIR}")
    print("\n[INFO] Usage:")
    print("   - Use /index command to create PROJECT_INDEX.json in any project")
    print("   - Reference with @PROJECT_INDEX.json for architectural awareness")
    print("   - The index updates automatically when you edit files")
    print(f"\n[INFO] For more information, see: {INSTALL_DIR / 'README.md'}")

if __name__ == '__main__':
    main()