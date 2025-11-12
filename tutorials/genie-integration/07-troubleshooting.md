# Troubleshooting Guide

Common issues and solutions for Genie MCP integrations.

## MCP Connection Issues

### "404 Not Found" Error

**Symptoms:**
- Bot can't connect to MCP server
- Error: "404 Not Found"

**Causes:**
- Incorrect workspace hostname
- Wrong Genie Space ID
- Genie not enabled in workspace

**Solutions:**
1. Verify workspace hostname in `.env`:
   ```bash
   DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
   ```
2. Check Genie Space ID is correct:
   ```bash
   GENIE_SPACE_ID=01f0be3dcc771e60ada71b6ec9f61870
   ```
3. Verify Genie is enabled:
   - Go to Databricks → SQL → Genie
   - Check you can access Genie spaces
4. Test MCP endpoint directly:
   ```bash
   curl https://your-workspace.cloud.databricks.com/api/2.0/mcp/genie/your-space-id
   ```

### "401 Unauthorized" Error

**Symptoms:**
- Authentication fails
- Error: "401 Unauthorized"

**Causes:**
- Invalid or expired token
- Missing credentials
- Incorrect authentication method

**Solutions:**
1. Check `.env` file has credentials:
   ```bash
   DATABRICKS_TOKEN=your-token
   # OR
   DATABRICKS_CLIENT_ID=your-client-id
   DATABRICKS_CLIENT_SECRET=your-client-secret
   ```
2. Verify token hasn't expired:
   - Go to Databricks → User Settings → Access Tokens
   - Check token expiration
   - Generate new token if needed
3. Test authentication:
   ```python
   from databricks.sdk import WorkspaceClient
   client = WorkspaceClient()
   print(client.current_user.me())
   ```
4. If using `~/.databrickscfg`:
   ```bash
   databricks configure --token
   ```

### "Tool not found" Error

**Symptoms:**
- MCP connection works but tool call fails
- Error: "Tool not found"

**Causes:**
- Incorrect tool name
- Tool name doesn't match space ID

**Solutions:**
1. Let client auto-discover tool name:
   ```python
   # Client will discover tool name automatically
   response = await mcp_client.ask_genie(space_id, question)
   ```
2. Verify tool name format:
   - Should be: `query_space_{space_id}`
   - Space ID must match exactly
3. Check MCP server tools:
   ```python
   mcp_client = DatabricksMCPClient(server_url, workspace_client)
   tools = mcp_client.list_tools()
   print([t.name for t in tools])
   ```

### Empty Response from Genie

**Symptoms:**
- MCP call succeeds but response is empty
- No data returned

**Causes:**
- Genie Space has no tables configured
- Query doesn't match available data
- Permissions issue

**Solutions:**
1. Check Genie Space configuration:
   - Go to Databricks → SQL → Genie → Your Space
   - Verify tables are selected
   - Check space instructions
2. Try simpler query:
   ```python
   response = await mcp_client.ask_genie(space_id, "What tables are available?")
   ```
3. Verify permissions:
   - Check Unity Catalog permissions
   - Ensure user can access tables
4. Check Genie Space logs:
   - Go to Genie Space → View logs
   - Look for errors

## Platform-Specific Issues

### Slack Bot Issues

#### Bot Not Responding

**Symptoms:**
- Bot starts but doesn't respond to messages

**Solutions:**
1. Check Event Subscriptions:
   - Go to Slack app → Event Subscriptions
   - Verify `app_mention` and `message.im` are subscribed
2. Verify Socket Mode:
   - Check Socket Mode is enabled
   - Verify `SLACK_APP_TOKEN` is correct
3. Check bot is installed:
   - Go to Slack workspace → Apps
   - Verify bot is installed
4. Review logs:
   ```bash
   # Check bot terminal for errors
   python slack_bot.py
   ```

#### Token Errors

**Symptoms:**
- "Invalid token" errors
- Authentication failures

**Solutions:**
1. Verify tokens in `.env`:
   ```bash
   SLACK_BOT_TOKEN=xoxb-...
   SLACK_APP_TOKEN=xapp-...
   ```
2. Check token prefixes:
   - Bot token: `xoxb-`
   - App token: `xapp-`
3. Regenerate tokens if needed:
   - Go to Slack app → OAuth & Permissions
   - Regenerate tokens

### Teams Bot Issues

#### Agents Playground Won't Connect

**Symptoms:**
- Can't connect to bot from Agents Playground

**Solutions:**
1. Verify bot is running:
   ```bash
   python teams_bot.py
   # Should show: "Listening on: http://localhost:3978/api/messages"
   ```
2. Check URL is correct:
   ```bash
   agentsplayground -e "http://localhost:3978/api/messages"
   ```
3. Verify port is available:
   ```bash
   lsof -i :3978
   # Should show your bot process
   ```
4. Check firewall:
   - Ensure localhost connections aren't blocked
   - Try different port if needed

#### Azure Deployment Issues

**Symptoms:**
- Bot deployed but not responding
- Errors in Azure logs

**Solutions:**
1. Check App Service logs:
   - Go to Azure Portal → App Service → Log stream
   - Look for errors
2. Verify environment variables:
   - Go to App Service → Configuration
   - Verify all variables are set
3. Check messaging endpoint:
   - Go to Azure Bot → Configuration
   - Verify endpoint URL is correct
4. Test health endpoint:
   ```bash
   curl https://your-app.azurewebsites.net/
   ```

## Code Issues

### Import Errors

**Symptoms:**
- "Module not found" errors
- Import failures

**Solutions:**
1. Verify virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Check Python path:
   ```python
   import sys
   print(sys.path)
   # Verify project root is included
   ```

### Async/Await Issues

**Symptoms:**
- "RuntimeError: This event loop is already running"
- Async errors

**Solutions:**
1. Use `asyncio.run()`:
   ```python
   if __name__ == "__main__":
       asyncio.run(main())
   ```
2. Avoid nested event loops
3. Use `asyncio.to_thread()` for sync operations:
   ```python
   result = await asyncio.to_thread(sync_function, args)
   ```

### JSON Parsing Errors

**Symptoms:**
- "JSON decode error"
- Response formatting fails

**Solutions:**
1. Check response structure:
   ```python
   print(raw_response[:500])  # Inspect response
   ```
2. Handle nested JSON:
   ```python
   outer = json.loads(raw_response)
   if "content" in outer:
       data = json.loads(outer["content"])
   ```
3. Add error handling:
   ```python
   try:
       data = json.loads(response)
   except json.JSONDecodeError:
       return "Unable to parse response"
   ```

## Performance Issues

### Slow Responses

**Symptoms:**
- Bot takes long time to respond
- Timeouts

**Solutions:**
1. Check Genie query complexity:
   - Simplify queries
   - Add timeouts
2. Monitor MCP connection:
   - Check network latency
   - Verify workspace connectivity
3. Optimize code:
   - Use async/await properly
   - Avoid blocking operations
4. Check Databricks cluster:
   - Ensure cluster is running
   - Check cluster performance

### Memory Issues

**Symptoms:**
- Bot crashes
- Memory errors

**Solutions:**
1. Limit conversation storage:
   ```python
   # Clear old conversations
   if len(conversations) > 1000:
       conversations.clear()
   ```
2. Monitor memory usage
3. Use efficient data structures

## Getting Help

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test MCP Connection

```python
import asyncio
from shared.mcp_client import create_mcp_client

async def test():
    client = create_mcp_client()
    response, _ = await client.ask_genie(
        "your-space-id",
        "What tables are available?"
    )
    print(response)

asyncio.run(test())
```

### Check Logs

- **Slack:** Check bot terminal output
- **Teams:** Check Azure App Service logs
- **MCP:** Check Databricks workspace logs

## Next Steps

- Review [Best Practices](08-best-practices.md)
- Check platform-specific documentation
- Test with simple queries first

