# Step 6: Testing Your Slack Bot

Comprehensive testing guide for your Slack bot.

## Test Checklist

- [ ] Bot starts successfully
- [ ] Bot responds to DMs
- [ ] Bot responds to @mentions
- [ ] Genie queries work
- [ ] Conversation context maintained
- [ ] Error handling works
- [ ] Help command works
- [ ] Reset command works

## Basic Tests

### Test 1: Bot Startup

**Run:**
```bash
python code/slack_bot.py
```

**Expected:**
```
============================================================
Starting Slack Genie Bot...
============================================================
Configuration valid
Genie Space: 01f0be3dcc771e60ada71b6ec9f61870

Bot is running... Send a DM or @mention me in a channel!
Press Ctrl+C to stop
============================================================
```

**If fails:**
- Check `.env` file has all required variables
- Verify tokens are correct
- Check Genie Space ID is valid

### Test 2: Direct Message

**Steps:**
1. Open Slack
2. Find your bot in app list
3. Send DM: `What tables are available?`

**Expected:**
- Bot responds with Genie results
- Response includes SQL query (if available)
- Results are formatted nicely

**If fails:**
- Check bot logs for errors
- Verify Genie Space has data
- Check MCP connection

### Test 3: Channel Mention

**Steps:**
1. Go to any channel
2. Type: `@Genie Bot what was Q4 revenue?`
3. Bot should respond in thread

**Expected:**
- Bot responds in thread
- Response formatted with blocks
- Question and answer clearly shown

**If fails:**
- Check `app_mention` event is subscribed
- Verify bot is in channel
- Check bot permissions

### Test 4: Conversation Context

**Steps:**
1. Send DM: `What was Q4 revenue?`
2. Send follow-up: `What about Q3?`

**Expected:**
- Second question understands context
- Genie maintains conversation

**If fails:**
- Check conversation ID is stored
- Verify conversation_id is passed to Genie

### Test 5: Help Command

**Steps:**
1. Send DM: `help`

**Expected:**
- Bot responds with help text
- Shows available commands

### Test 6: Reset Command

**Steps:**
1. Send DM: `reset`
2. Send question: `What was revenue?`

**Expected:**
- Bot confirms reset
- New conversation starts fresh

### Test 7: Error Handling

**Steps:**
1. Temporarily break `.env` (wrong token)
2. Try to start bot

**Expected:**
- Bot shows clear error message
- Doesn't crash silently

## Advanced Tests

### Test 8: Multiple Users

**Steps:**
1. Have multiple users DM the bot
2. Each asks different questions

**Expected:**
- Each user gets separate conversation context
- No cross-contamination

### Test 9: Concurrent Requests

**Steps:**
1. Send multiple questions rapidly
2. Check responses

**Expected:**
- All requests handled
- No errors or timeouts

### Test 10: Long Queries

**Steps:**
1. Send complex question: `Show me all customers with orders over $10,000 in Q4, grouped by region, sorted by total revenue`

**Expected:**
- Bot handles long queries
- Response formatted properly
- No truncation issues

## Integration Tests

### Test with Real Genie Space

**Prerequisites:**
- Genie Space with real data
- Access to workspace

**Steps:**
1. Test with actual business questions
2. Verify results match expectations
3. Check SQL queries are correct

### Test Performance

**Steps:**
1. Measure response time
2. Test with various query complexities
3. Monitor resource usage

**Expected:**
- Response time < 10 seconds for most queries
- No memory leaks
- Stable performance

## Production Readiness Checklist

- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Environment variables secured
- [ ] Bot tested with real users
- [ ] Performance acceptable
- [ ] Monitoring set up
- [ ] Documentation complete

## Common Issues and Solutions

### Bot Not Responding

**Symptoms:**
- Bot starts but doesn't respond to messages

**Solutions:**
- Check Event Subscriptions are enabled
- Verify bot token is correct
- Check bot is installed in workspace
- Review logs for errors

### Genie Errors

**Symptoms:**
- Bot responds but Genie queries fail

**Solutions:**
- Verify Genie Space ID is correct
- Check MCP connection
- Verify workspace permissions
- Test MCP connection directly

### Formatting Issues

**Symptoms:**
- Responses not formatted properly

**Solutions:**
- Check `format_genie_response` function
- Verify JSON parsing
- Test with sample responses

## Next Steps

- Review [Best Practices](../08-best-practices.md)
- Check [Troubleshooting](../07-troubleshooting.md)
- Deploy to production when ready

