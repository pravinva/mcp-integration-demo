#!/usr/bin/env python3
"""
Helper script to find or guide creation of Genie Space.

Genie Spaces cannot be created programmatically - they must be created
manually through the Databricks UI. This script helps you:
1. List existing Genie Spaces
2. Find a space by name
3. Get instructions for creating a new space
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from databricks.sdk import WorkspaceClient
from shared.config import get_workspace_client


def list_genie_spaces():
    """List all Genie Spaces in the workspace"""
    try:
        workspace_client = get_workspace_client()
        
        print("🔍 Checking Genie API availability...")
        
        # Check if Genie API is available
        if not hasattr(workspace_client, 'genie'):
            print("❌ Genie API not available in SDK")
            print("   This might mean:")
            print("   - Genie is not enabled in your workspace")
            print("   - SDK version doesn't support Genie")
            print("   - You don't have permissions")
            return None
        
        genie = workspace_client.genie
        
        print("✅ Genie API found")
        print("\n📋 Listing Genie Spaces...\n")
        
        # Try to list spaces
        try:
            spaces_response = genie.list_spaces()
            
            # Handle different response structures
            if hasattr(spaces_response, 'spaces'):
                spaces = spaces_response.spaces
            elif hasattr(spaces_response, 'items'):
                spaces = spaces_response.items
            elif isinstance(spaces_response, list):
                spaces = spaces_response
            else:
                spaces = [spaces_response] if spaces_response else []
            
            if spaces:
                print(f"Found {len(spaces)} Genie Space(s):\n")
                for i, space in enumerate(spaces, 1):
                    space_name = getattr(space, 'title', getattr(space, 'name', 'Unknown'))
                    space_id = getattr(space, 'space_id', getattr(space, 'id', 'Unknown'))
                    print(f"{i}. {space_name}")
                    print(f"   ID: {space_id}")
                    print()
                
                return spaces
            else:
                print("No Genie Spaces found.")
                print("\nYou'll need to create one manually (see instructions below).")
                return []
                
        except Exception as e:
            print(f"⚠️  Could not list spaces: {e}")
            print("\nThis might mean:")
            print("  - Genie API requires different authentication")
            print("  - You don't have permissions to list spaces")
            print("  - Genie is not enabled in your workspace")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def find_space_by_name(name: str):
    """Find a Genie Space by name"""
    spaces = list_genie_spaces()
    
    if not spaces:
        return None
    
    name_lower = name.lower().strip()
    
    for space in spaces:
        space_name = getattr(space, 'title', getattr(space, 'name', ''))
        if space_name.lower() == name_lower:
            space_id = getattr(space, 'space_id', getattr(space, 'id', ''))
            print(f"\n✅ Found: {space_name}")
            print(f"   Space ID: {space_id}")
            print(f"\n📝 Add this to your .env file:")
            print(f"   GENIE_SPACE_ID={space_id}")
            return space_id
    
    print(f"\n❌ Space '{name}' not found")
    return None


def print_creation_instructions():
    """Print instructions for creating a Genie Space manually"""
    print("\n" + "=" * 70)
    print("📝 How to Create a Genie Space Manually")
    print("=" * 70)
    print()
    print("Genie Spaces cannot be created programmatically.")
    print("You must create them through the Databricks UI.\n")
    print("Steps:")
    print("1. Go to your Databricks workspace")
    print("2. Click on 'Genie' in the left sidebar (or go to SQL → Genie)")
    print("3. Click the 'New' button (upper-right corner)")
    print("4. Configure your space:")
    print("   - Name: Choose a descriptive name")
    print("   - Catalog: Select your catalog (e.g., demo_retail)")
    print("   - Schema: Select your schema (e.g., ecommerce)")
    print("   - Tables: Select tables to include")
    print("5. Click 'Create'")
    print()
    print("After creating:")
    print("- The Space ID will be in the URL: /sql/genie/{space_id}")
    print("- Or run this script again to list all spaces")
    print("- Add GENIE_SPACE_ID to your .env file")
    print()
    print("=" * 70)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Find or guide creation of Genie Spaces"
    )
    parser.add_argument(
        '--find',
        type=str,
        help='Find a space by name'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all Genie Spaces'
    )
    parser.add_argument(
        '--instructions',
        action='store_true',
        help='Show instructions for creating a Genie Space'
    )
    
    args = parser.parse_args()
    
    if args.find:
        find_space_by_name(args.find)
    elif args.list:
        list_genie_spaces()
    elif args.instructions:
        print_creation_instructions()
    else:
        # Default: list spaces and show instructions
        spaces = list_genie_spaces()
        if not spaces:
            print_creation_instructions()


if __name__ == "__main__":
    main()

