# Step 3: Test with Agents Playground

Test your Teams bot in a Teams-like interface using Agents Playground.

## Prerequisites

- Bot code implemented
- Bot running on `http://localhost:3978/api/messages`
- Agents Playground installed

## Step-by-Step Testing

### 1. Start Your Bot

In terminal 1:

```bash
cd tutorials/genie-integration/06-teams-integration/code
python teams_bot.py
```

**Verify:**
- Bot shows "Listening on: http://localhost:3978/api/messages"
- No errors in console

### 2. Launch Agents Playground

In terminal 2:

```bash
agentsplayground -e "http://localhost:3978/api/messages" -c "emulator"
```

**What happens:**
- Browser opens automatically
- You see Teams-like chat interface
- Bot is connected

### 3. Test Basic Functionality

#### Test 1: Welcome Message

**Action:** Connect to bot

**Expected:**
- Welcome message appears
- Bot introduces itself

#### Test 2: Simple Query

**Action:** Type: `What tables are available?`

**Expected:**
- Typing indicator appears
- Bot responds with Genie results
- Response formatted nicely

#### Test 3: Follow-up Question

**Action:** After first response, type: `What about customers?`

**Expected:**
- Bot maintains context
- Response relates to previous question

#### Test 4: Help Command

**Action:** Type: `/help`

**Expected:**
- Bot shows help text
- Lists available commands

#### Test 5: Reset Command

**Action:** Type: `/reset`

**Expected:**
- Bot confirms reset
- Conversation context cleared

### 4. Test Error Handling

#### Test 6: Invalid Query

**Action:** Type: `asdfghjkl`

**Expected:**
- Bot handles error gracefully
- Shows error message
- Doesn't crash

#### Test 7: Empty Message

**Action:** Send empty message

**Expected:**
- Bot handles gracefully
- No errors

## What You'll See

### Agents Playground Interface

- **Left sidebar:** Chat list (like Teams)
- **Main area:** Conversation with bot
- **Input box:** Type messages here
- **Send button:** Send message

### Bot Responses

- **Typing indicator:** Shows bot is thinking
- **Formatted messages:** Markdown formatting
- **SQL queries:** Code blocks
- **Results:** Formatted tables

## Testing Checklist

- [ ] Bot starts successfully
- [ ] Agents Playground connects
- [ ] Welcome message appears
- [ ] Simple query works
- [ ] Response formatted correctly
- [ ] Follow-up questions work
- [ ] Help command works
- [ ] Reset command works
- [ ] Error handling works
- [ ] Conversation context maintained

## Advanced Testing

### Test Multiple Conversations

1. Open multiple Agents Playground windows
2. Each has separate conversation
3. Verify no cross-contamination

### Test Performance

1. Send multiple rapid queries
2. Verify all handled correctly
3. Check response times

### Test Long Queries

1. Send complex question
2. Verify response complete
3. Check formatting preserved

## Troubleshooting

### Bot Not Responding

**Check:**
1. Bot terminal shows no errors
2. Agents Playground connected
3. URL is correct: `http://localhost:3978/api/messages`

**Solution:**
- Restart bot
- Reconnect Agents Playground
- Check logs

### Responses Not Formatted

**Check:**
1. `format_genie_response` function
2. Genie response structure
3. JSON parsing

**Solution:**
- Check bot logs
- Test Genie response directly
- Verify formatting function

### Conversation Context Lost

**Check:**
1. Conversation ID storage
2. Conversation ID passed to Genie
3. Storage mechanism

**Solution:**
- Verify `conversations` dictionary
- Check conversation ID generation
- Test with simple queries first

## Next Steps

Once testing is complete:

- [Production Deployment](04-production-deployment.md) - Deploy to Azure
- [Add to Teams](05-add-to-teams.md) - Add to real Teams

## Comparison: Agents Playground vs Real Teams

| Feature | Agents Playground | Real Teams |
|---------|------------------|------------|
| **UI** | Teams-like | Real Teams |
| **Cost** | FREE | Azure costs |
| **Setup** | 5 minutes | 30+ minutes |
| **Use Case** | Development | Production |
| **Features** | Basic | Full Teams |

**Recommendation:** Use Agents Playground for development, deploy to Azure for production.

