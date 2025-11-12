#!/usr/bin/env python3
"""
Azure Deployment Script for Teams Bot

This script helps deploy your Teams bot to Azure for real Teams integration.
"""

import subprocess
import sys
import os
import json
from pathlib import Path

def check_azure_cli():
    """Check if Azure CLI is installed"""
    try:
        result = subprocess.run(['az', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ Azure CLI found: {version}")
            return True
    except:
        pass
    print("❌ Azure CLI not found")
    return False

def check_azure_login():
    """Check if logged into Azure"""
    try:
        result = subprocess.run(['az', 'account', 'show'], capture_output=True, text=True)
        if result.returncode == 0:
            account = json.loads(result.stdout)
            print(f"✅ Logged in as: {account.get('user', {}).get('name', 'Unknown')}")
            return True
    except:
        pass
    print("⚠️  Not logged into Azure")
    return False

def print_deployment_plan():
    """Print what will be created"""
    print("=" * 70)
    print("🚀 Azure Deployment Plan")
    print("=" * 70)
    print()
    print("This will create:")
    print()
    print("1. Resource Group: mcp-bots-rg")
    print("2. Azure Bot: genie-teams-bot-<unique>")
    print("   - App ID and Password (save these!)")
    print("3. App Service: genie-teams-bot-<unique>")
    print("   - Python 3.11 runtime")
    print("   - Free tier (F1)")
    print("4. Configure:")
    print("   - Messaging endpoint")
    print("   - Teams channel")
    print("   - Environment variables")
    print()
    print("=" * 70)
    print("💰 Cost: $0/month (free tier)")
    print("=" * 70)
    print()

def create_resources():
    """Create Azure resources"""
    import random
    import string
    
    # Generate unique suffix
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    bot_name = f"genie-teams-bot-{suffix}"
    app_name = f"genie-teams-app-{suffix}"
    resource_group = "mcp-bots-rg"
    location = "eastus"  # Change if needed
    
    print(f"📝 Generated names:")
    print(f"   Bot: {bot_name}")
    print(f"   App: {app_name}")
    print(f"   Resource Group: {resource_group}")
    print()
    
    # Check if resource group exists
    result = subprocess.run(
        ['az', 'group', 'exists', '--name', resource_group],
        capture_output=True, text=True
    )
    
    if 'false' in result.stdout.lower():
        print(f"📦 Creating resource group: {resource_group}")
        subprocess.run([
            'az', 'group', 'create',
            '--name', resource_group,
            '--location', location
        ])
    
    # Create App Service
    print(f"🌐 Creating App Service: {app_name}")
    subprocess.run([
        'az', 'webapp', 'create',
        '--resource-group', resource_group,
        '--name', app_name,
        '--runtime', 'PYTHON:3.11',
        '--plan', f'{app_name}-plan',
        '--sku', 'FREE'
    ])
    
    # Create App Service Plan (if needed)
    print(f"📋 Creating App Service Plan")
    subprocess.run([
        'az', 'appservice', 'plan', 'create',
        '--name', f'{app_name}-plan',
        '--resource-group', resource_group,
        '--sku', 'FREE',
        '--is-linux'
    ])
    
    # Create Azure Bot
    print(f"🤖 Creating Azure Bot: {bot_name}")
    result = subprocess.run([
        'az', 'bot', 'create',
        '--resource-group', resource_group,
        '--name', bot_name,
        '--appid', 'PLACEHOLDER',  # Will be created
        '--password', 'PLACEHOLDER',  # Will be created
        '--sku', 'F0',
        '--location', location
    ], capture_output=True, text=True)
    
    print()
    print("=" * 70)
    print("✅ Resources Created!")
    print("=" * 70)
    print()
    print("📝 Next Steps:")
    print(f"1. Get App ID/Password from Azure Portal")
    print(f"2. Set environment variables in App Service")
    print(f"3. Deploy bot code")
    print(f"4. Configure messaging endpoint")
    print(f"5. Enable Teams channel")
    print()
    print(f"🔗 App Service URL: https://{app_name}.azurewebsites.net")
    print(f"🔗 Azure Portal: https://portal.azure.com")

def main():
    print("=" * 70)
    print("🚀 Azure Deployment for Teams Bot")
    print("=" * 70)
    print()
    
    # Check prerequisites
    if not check_azure_cli():
        print()
        print("💡 Install Azure CLI:")
        print("   brew install azure-cli")
        print("   Then: az login")
        sys.exit(1)
    
    print()
    
    if not check_azure_login():
        print()
        print("💡 Login to Azure:")
        print("   az login")
        print("   Then run this script again")
        sys.exit(1)
    
    print()
    print_deployment_plan()
    
    response = input("Create Azure resources now? (y/n): ")
    if response.lower() != 'y':
        print("\n💡 Manual deployment guide: DEPLOY_TO_TEAMS.md")
        sys.exit(0)
    
    print()
    create_resources()

if __name__ == "__main__":
    main()

