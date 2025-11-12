#!/usr/bin/env python3
"""
Prepare Teams Bot for Azure Deployment

This script creates a deployment-ready ZIP file for Azure App Service.
"""

import zipfile
import os
import sys
from pathlib import Path

def create_deployment_package():
    """Create deployment ZIP for Azure"""
    project_root = Path(__file__).parent.parent.parent
    teams_dir = project_root / "demos" / "03-teams"
    output_file = project_root / "bot-deploy.zip"
    
    print("=" * 70)
    print("📦 Preparing Teams Bot Deployment Package")
    print("=" * 70)
    print()
    
    # Files to include
    include_files = [
        "teams_bot.py",
        "__init__.py" if (teams_dir / "__init__.py").exists() else None,
    ]
    
    # Files to exclude
    exclude_patterns = [
        "*.pyc",
        "__pycache__",
        "*.log",
        "*.md",
        "test_*.py",
        "quick_start.py",
        "launch_playground.py",
        "deploy_*.py",
        "start_all.py",
        "show_chat_guide.py",
        "download_emulator.py",
        ".env",
        ".git",
    ]
    
    print("📝 Creating deployment package...")
    print(f"   Source: {teams_dir}")
    print(f"   Output: {output_file}")
    print()
    
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add bot file
        bot_file = teams_dir / "teams_bot.py"
        if bot_file.exists():
            zipf.write(bot_file, "teams_bot.py")
            print(f"✅ Added: teams_bot.py")
        
        # Add shared directory
        shared_dir = project_root / "shared"
        if shared_dir.exists():
            for file in shared_dir.rglob("*.py"):
                if "__pycache__" not in str(file):
                    arcname = f"shared/{file.relative_to(shared_dir)}"
                    zipf.write(file, arcname)
                    print(f"✅ Added: {arcname}")
        
        # Add requirements.txt
        requirements = project_root / "requirements.txt"
        if requirements.exists():
            zipf.write(requirements, "requirements.txt")
            print(f"✅ Added: requirements.txt")
    
    print()
    print("=" * 70)
    print("✅ Deployment Package Created!")
    print("=" * 70)
    print()
    print(f"📦 File: {output_file}")
    print(f"📊 Size: {output_file.stat().st_size / 1024:.1f} KB")
    print()
    print("🚀 Next Steps:")
    print("1. Go to Azure Portal → Your App Service")
    print("2. Deployment Center → Local Git/ZIP")
    print(f"3. Upload: {output_file.name}")
    print("4. Set environment variables")
    print("5. Configure messaging endpoint")
    print()
    print("📚 See: REAL_TEAMS_QUICK.md for complete guide")

if __name__ == "__main__":
    try:
        create_deployment_package()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

