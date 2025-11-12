"""
Direct Genie API Integration - WITHOUT MCP

This shows how Genie integration works without MCP protocol.
Notice the complexity: manual REST calls, polling, error handling.

Compare this to shared/mcp_client.py which is ~50 lines!
"""

import requests
import time
from typing import Optional
from databricks.sdk import WorkspaceClient


class DirectGenieClient:
    """
    Direct Genie API client - NO MCP protocol.
    
    This is what you'd need to write for EACH platform:
    - CLI version
    - Slack version  
    - Teams version
    - Claude version
    
    Each with slightly different error handling, logging, etc.
    Result: 4 × 200 lines = 800 lines just for Genie!
    """
    
    def __init__(self, workspace_client: WorkspaceClient, space_id: str):
        self.workspace_client = workspace_client
        self.space_id = space_id
        self.host = workspace_client.config.host
        self.token = workspace_client.config.token
    
    def _get_headers(self):
        """Get authentication headers"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def start_conversation(self, message: str, conversation_id: Optional[str] = None) -> tuple[str, str]:
        """
        Start a Genie conversation WITHOUT MCP.
        
        Steps:
        1. POST to start conversation
        2. Get conversation_id and message_id
        3. Poll for completion (manual polling!)
        4. Extract response
        
        This is ~50 lines. With MCP, it's 3 lines!
        """
        url = f"{self.host}/api/2.0/genie/conversations/{self.space_id}/messages"
        
        payload = {
            "message": message
        }
        
        if conversation_id:
            payload["conversation_id"] = conversation_id
        
        # Step 1: Start conversation
        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            conv_id = data.get("conversation_id")
            msg_id = data.get("message_id")
            
            if not conv_id or not msg_id:
                raise ValueError("Missing conversation_id or message_id in response")
            
            # Step 2: Poll for completion (manual polling logic!)
            max_attempts = 60  # 60 seconds timeout
            attempt = 0
            
            while attempt < max_attempts:
                # Check status
                status_url = f"{self.host}/api/2.0/genie/conversations/{self.space_id}/messages/{msg_id}"
                status_response = requests.get(
                    status_url,
                    headers=self._get_headers(),
                    timeout=10
                )
                status_response.raise_for_status()
                
                status_data = status_response.json()
                status = status_data.get("status")
                
                if status == "COMPLETED":
                    # Extract response text
                    attachments = status_data.get("attachments", [])
                    if attachments and len(attachments) > 0:
                        response_text = attachments[0].get("text", "")
                        return response_text, conv_id
                    else:
                        return "No response received", conv_id
                
                elif status == "FAILED":
                    error_msg = status_data.get("error", "Unknown error")
                    raise Exception(f"Genie query failed: {error_msg}")
                
                # Still processing, wait and retry
                time.sleep(1)
                attempt += 1
            
            # Timeout
            raise TimeoutError("Genie query timed out after 60 seconds")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP error calling Genie API: {str(e)}")
        except Exception as e:
            raise Exception(f"Error querying Genie: {str(e)}")
    
    def list_conversations(self) -> list:
        """List all conversations - more manual API calls"""
        url = f"{self.host}/api/2.0/genie/conversations/{self.space_id}"
        
        try:
            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("conversations", [])
        except Exception as e:
            raise Exception(f"Error listing conversations: {str(e)}")
    
    def provide_feedback(self, message_id: str, feedback: str) -> bool:
        """Provide feedback - yet another manual API call"""
        url = f"{self.host}/api/2.0/genie/conversations/{self.space_id}/messages/{message_id}/feedback"
        
        payload = {
            "feedback": feedback
        }
        
        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return True
        except Exception as e:
            raise Exception(f"Error providing feedback: {str(e)}")


# Example usage (compare to shared/mcp_client.py!)
if __name__ == "__main__":
    from databricks.sdk import WorkspaceClient
    
    # Setup (same as MCP version)
    workspace_client = WorkspaceClient(profile="DEFAULT")
    space_id = "your-space-id"
    
    # Create client
    client = DirectGenieClient(workspace_client, space_id)
    
    # Query (compare to: await mcp_client.ask_genie(...))
    response, conv_id = client.start_conversation("What was Q4 revenue?")
    print(f"Response: {response}")
    print(f"Conversation ID: {conv_id}")
    
    # Follow-up (compare to: await mcp_client.ask_genie(..., conv_id))
    response2, _ = client.start_conversation("What about Q3?", conv_id)
    print(f"Follow-up: {response2}")

