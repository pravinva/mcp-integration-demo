#!/usr/bin/env python3
"""
Azure Deployment Helper for Teams Bot

This script helps you deploy to Azure for real Teams integration.
"""

import subprocess
import sys
import os

def check_azure_cli():
    """Check if Azure CLI is installed"""
    try:
        result = subprocess.run(['az', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Azure CLI found")
            return True
    except:
        pass
    print("⚠️  Azure CLI not found")
    return False

def print_deployment_options():
    """Print deployment options"""
    print("=" * 70)
    print("🚀 Deploy Teams Bot to Real Microsoft Teams")
    print("=" * 70)
    print()
    print("You have 3 options:")
    print()
    print("1️⃣  Azure Portal (Easiest - No CLI needed)")
    print("   - Go to portal.azure.com")
    print("   - Create Azure Bot + App Service")
    print("   - Deploy via ZIP upload")
    print("   - Time: ~30 minutes")
    print()
    print("2️⃣  Azure CLI (Faster - Automated)")
    print("   - Install: brew install azure-cli")
    print("   - Login: az login")
    print("   - Run deployment script")
    print("   - Time: ~15 minutes")
    print()
    print("3️⃣  Manual Deployment (Most Control)")
    print("   - Follow step-by-step guide")
    print("   - Full control over resources")
    print("   - Time: ~45 minutes")
    print()
    print("=" * 70)
    print("📚 Guides Available:")
    print("=" * 70)
    print()
    print("✅ REAL_TEAMS_SETUP.md - Step-by-step Azure Portal guide")
    print("✅ AZURE_DEPLOYMENT.md - Complete deployment guide")
    print()
    print("=" * 70)
    print("💡 Quick Start:")
    print("=" * 70)
    print()
    print("1. Sign up for Azure: https://azure.microsoft.com/free/")
    print("2. Follow: REAL_TEAMS_SETUP.md")
    print("3. Deploy bot to Azure")
    print("4. Add to Teams!")
    print()

def main():
    print_deployment_options()
    
    # Check Azure CLI
    has_azure_cli = check_azure_cli()
    
    if has_azure_cli:
        print()
        print("✅ Azure CLI detected!")
        print("   You can use automated deployment scripts")
    else:
        print()
        print("💡 Install Azure CLI for faster deployment:")
        print("   brew install azure-cli")
        print("   Then: az login")

if __name__ == "__main__":
    main()

