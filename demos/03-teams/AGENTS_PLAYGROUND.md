# Teams Bot - Microsoft 365 Agents Playground Setup

## 🎯 New Tool: Agents Playground

**Bot Framework Emulator is deprecated** (retiring end of 2025).  
**Use Microsoft 365 Agents Playground instead!**

Reference: https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/test-with-toolkit-project

---

## 📥 Install Agents Playground

### Option 1: Install via npm (Recommended)

```bash
# Install Node.js if needed (check: node --version)
# Download from: https://nodejs.org/

# Install Agents Playground globally
npm install -g @microsoft/m365agentsplayground
```

### Option 2: Install Standalone Binary (Mac)

```bash
# For Mac (using Homebrew or direct download)
# Check: https://github.com/OfficeDev/microsoft-365-agents-toolkit
```

### Option 3: Install via Homebrew (if available)

```bash
# Check if available
brew search agentsplayground
```

---

## 🚀 Quick Start

### Step 1: Start Your Bot

```bash
cd demos/03-teams
python test_teams_bot.py
```

Bot will run on: `http://localhost:3978/api/messages`

### Step 2: Launch Agents Playground

**Basic (Anonymous Mode):**
```bash
agentsplayground -e "http://localhost:3978/api/messages" -c "emulator"
```

**With Authentication (if needed):**
```bash
agentsplayground -e "http://localhost:3978/api/messages" -c "emulator" \
  --client-id "your-client-id" \
  --client-secret "your-client-secret" \
  --tenant-id "your-tenant-id"
```

### Step 3: Start Chatting!

The Agents Playground will open in your browser. Start chatting!

---

## 🔧 Configuration Options

### Command Line Options

```bash
agentsplayground \
  -e "http://localhost:3978/api/messages" \  # Your bot endpoint
  -c "emulator" \                             # Channel: emulator, webchat, msteams
  --client-id "your-client-id" \             # Optional: for auth
  --client-secret "your-client-secret" \     # Optional: for auth
  --tenant-id "your-tenant-id"               # Optional: for auth
```

### Environment Variables (Alternative)

```bash
export BOT_ENDPOINT="http://localhost:3978/api/messages"
export DEFAULT_CHANNEL_ID="emulator"
export AUTH_CLIENT_ID="your-client-id"        # Optional
export AUTH_CLIENT_SECRET="your-client-secret" # Optional
export AUTH_TENANT_ID="your-tenant-id"        # Optional

agentsplayground
```

---

## 📋 Channel Options

The `-c` (channel-id) option supports:

- **`emulator`** - Basic emulator (like Bot Framework Emulator)
- **`webchat`** - Web chat interface
- **`msteams`** - Microsoft Teams interface

**For local testing, use `emulator`:**

```bash
agentsplayground -e "http://localhost:3978/api/messages" -c "emulator"
```

---

## ✅ Quick Test

1. **Start bot:**
   ```bash
   cd demos/03-teams
   python test_teams_bot.py
   ```

2. **Launch Agents Playground:**
   ```bash
   agentsplayground -e "http://localhost:3978/api/messages" -c "emulator"
   ```

3. **Chat!** Try:
   - `What was Q4 revenue?`
   - `search MCP tutorial`
   - `calculate 50000 Enterprise`
   - `/help`

---

## 🆚 Agents Playground vs Bot Framework Emulator

| Feature | Bot Framework Emulator | Agents Playground |
|---------|------------------------|-------------------|
| **Status** | ⚠️ Deprecated (retiring 2025) | ✅ Active |
| **Installation** | Download .dmg | `npm install -g` |
| **Channels** | Emulator only | emulator, webchat, msteams |
| **Future Support** | ❌ No updates | ✅ Actively maintained |
| **Microsoft Support** | Ending 2025 | ✅ Supported |

---

## 🔄 Migration from Bot Framework Emulator

**Old way (deprecated):**
1. Download Bot Framework Emulator .dmg
2. Install app
3. Open app → Connect to bot

**New way (Agents Playground):**
1. `npm install -g @microsoft/m365agentsplayground`
2. `agentsplayground -e "http://localhost:3978/api/messages" -c "emulator"`
3. Browser opens → Start chatting!

**Much simpler!** 🚀

---

## 💡 Pro Tips

1. **Use `emulator` channel** for local testing (like old Bot Framework Emulator)
2. **No authentication needed** for local testing (anonymous mode)
3. **Browser-based** - Opens in your default browser
4. **Multiple channels** - Test with different interfaces

---

## 📚 Resources

- **Official Docs:** https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/test-with-toolkit-project
- **GitHub:** https://github.com/OfficeDev/microsoft-365-agents-toolkit
- **Help:** `agentsplayground --help`

---

## ✅ Summary

**Old:** Bot Framework Emulator (deprecated)  
**New:** Microsoft 365 Agents Playground ✅

**Install:**
```bash
npm install -g @microsoft/m365agentsplayground
```

**Run:**
```bash
agentsplayground -e "http://localhost:3978/api/messages" -c "emulator"
```

**That's it!** Much simpler than the old emulator! 🎉

