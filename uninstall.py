#!/usr/bin/env python3
"""
CLAUDE-CODE-PROJECT-INDEX (Windows) Uninstaller
Windows-specific uninstaller for PROJECT_INDEX tool
"""

import os
import sys
import json
import shutil
from pathlib import Path

# Set UTF-8 encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

INSTALL_DIR = Path.home() / ".claude-code-project-index"

def print_header():
    """Print uninstallation header"""
    print("CLAUDE-CODE-PROJECT-INDEX (Windows) Uninstaller")
    print("=" * 50)
    print()

def remove_hooks(settings_file):
    """Remove PROJECT_INDEX hooks from settings.json"""
    if not settings_file.exists():
        return False
    
    print("Removing hooks from settings.json...")
    
    try:
        with open(settings_file, 'r') as f:
            settings = json.load(f)
        
        if 'hooks' not in settings:
            return False
        
        modified = False
        
        # Remove PostToolUse hooks
        if 'PostToolUse' in settings['hooks']:
            original_len = len(settings['hooks']['PostToolUse'])
            settings['hooks']['PostToolUse'] = [
                hook for hook in settings['hooks']['PostToolUse']
                if not any('update_index.py' in str(h.get('command', '')) or 
                          'project_index' in str(h.get('command', ''))
                          for h in hook.get('hooks', []))
            ]
            if len(settings['hooks']['PostToolUse']) < original_len:
                modified = True
        
        # Remove Stop hooks
        if 'Stop' in settings['hooks']:
            original_len = len(settings['hooks']['Stop'])
            settings['hooks']['Stop'] = [
                hook for hook in settings['hooks']['Stop']
                if not any('reindex_if_needed.py' in str(h.get('command', '')) or
                          'project_index' in str(h.get('command', ''))
                          for h in hook.get('hooks', []))
            ]
            if len(settings['hooks']['Stop']) < original_len:
                modified = True
        
        if modified:
            # Backup before modifying
            backup_file = settings_file.with_suffix('.json.uninstall-backup')
            shutil.copy2(settings_file, backup_file)
            print(f"   [OK] Backed up settings to {backup_file}")
            
            # Write modified settings
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            print("   [OK] Removed PROJECT_INDEX hooks")
            return True
        else:
            print("   [INFO] No PROJECT_INDEX hooks found")
            return False
            
    except Exception as e:
        print(f"   [WARNING] Error modifying settings.json: {e}")
        return False

def remove_command():
    """Remove the /index command"""
    commands_dir = Path.home() / '.claude' / 'commands'
    index_cmd = commands_dir / 'index.md'
    
    if index_cmd.exists():
        print("Removing /index command...")
        index_cmd.unlink()
        print("   [OK] Removed /index command")
        return True
    else:
        print("   [INFO] /index command not found")
        return False

def remove_installation():
    """Remove the installation directory"""
    if INSTALL_DIR.exists():
        print(f"Removing installation directory: {INSTALL_DIR}")
        shutil.rmtree(INSTALL_DIR)
        print("   [OK] Removed installation directory")
        return True
    else:
        print(f"   [INFO] Installation directory not found: {INSTALL_DIR}")
        return False

def main():
    """Main uninstallation process"""
    print_header()
    
    # Check if installed
    if not INSTALL_DIR.exists():
        print("[WARNING] PROJECT_INDEX does not appear to be installed")
        print(f"   Installation directory not found: {INSTALL_DIR}")
        print("\nChecking for partial installation...")
    
    # Confirm uninstallation
    if sys.stdin.isatty():
        print("This will remove:")
        print(f"  - Installation directory: {INSTALL_DIR}")
        print("  - /index command")
        print("  - Hooks from settings.json")
        print()
        
        response = input("Continue with uninstallation? (y/N): ")
        if response.lower() != 'y':
            print("Uninstallation cancelled")
            return
    
    print()
    
    # Remove components
    removed_something = False
    
    # Remove hooks
    settings_file = Path.home() / '.claude' / 'settings.json'
    if remove_hooks(settings_file):
        removed_something = True
    
    # Remove command
    if remove_command():
        removed_something = True
    
    # Remove installation directory
    if remove_installation():
        removed_something = True
    
    # Print summary
    print("\n" + "=" * 50)
    if removed_something:
        print("[SUCCESS] PROJECT_INDEX uninstalled successfully!")
        print("=" * 50)
        print("\n[INFO] Note:")
        print("   - Your PROJECT_INDEX.json files in projects remain untouched")
        print("   - Settings backup saved (if hooks were removed)")
        print("\n[INFO] To reinstall:")
        print("   python install.py")
    else:
        print("[INFO] Nothing to uninstall")
        print("=" * 50)

if __name__ == '__main__':
    main()