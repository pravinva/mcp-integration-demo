# ✅ Updated to Microsoft 365 Agents Playground

## 🎯 What Changed

**Bot Framework Emulator is deprecated** (retiring end of 2025)  
**Microsoft 365 Agents Playground is now the recommended tool**

Reference: https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/test-with-toolkit-project

---

## ✅ Installation Status

- ✅ **Agents Playground installed:** `@microsoft/m365agentsplayground@0.2.20`
- ✅ **Node.js version:** v25.1.0 (compatible)
- ✅ **npm version:** 11.6.2

---

## 🚀 How to Use

### Step 1: Start Your Bot

```bash
cd demos/03-teams
python test_teams_bot.py
```

Keep this terminal open!

### Step 2: Launch Agents Playground

**In a new terminal:**

```bash
agentsplayground -e "http://localhost:3978/api/messages" -c "emulator"
```

**Browser will open automatically!** Start chatting!

---

## 🆚 What's Different

### Old Way (Deprecated)
```
1. Download Bot Framework Emulator .dmg
2. Install app
3. Open app
4. Click "Open Bot"
5. Enter URL
6. Click "Connect"
```

### New Way (Agents Playground)
```
1. npm install -g @microsoft/m365agentsplayground
2. agentsplayground -e "http://localhost:3978/api/messages" -c "emulator"
3. Browser opens automatically!
```

**Much simpler!** 🚀

---

## 💬 Test Commands

Once Agents Playground opens:

- `What was Q4 revenue?`
- `search MCP tutorial`
- `calculate 50000 Enterprise`
- `/help`
- `/reset`

---

## 🐛 If You See Errors

**Runtime Error (TypeError):**
- This is a known issue with some Node.js versions
- Try: Update Node.js to latest LTS
- Or: Use Bot Framework Emulator temporarily (still works, just deprecated)

**Command Not Found:**
- Verify: `npm list -g @microsoft/m365agentsplayground`
- Reinstall: `npm install -g @microsoft/m365agentsplayground`

---

## 📚 Updated Files

All documentation updated:
- ✅ `README.md` - Uses Agents Playground
- ✅ `AGENTS_PLAYGROUND.md` - Complete guide
- ✅ `test_teams_bot.py` - Updated instructions
- ✅ `quick_start.py` - Checks for Agents Playground
- ✅ `launch_playground.py` - Helper script

---

## ✅ Summary

**Status:** ✅ Agents Playground installed and ready!

**To test:**
1. Start bot: `python test_teams_bot.py`
2. Launch: `agentsplayground -e "http://localhost:3978/api/messages" -c "emulator"`
3. Chat!

**Note:** If Agents Playground has issues, Bot Framework Emulator still works (just deprecated). Both tools work with your bot!

---

## 🎉 Ready!

Your bot is updated to use the modern Agents Playground! 🚀

