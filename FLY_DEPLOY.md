# 🚀 FLY.IO DEPLOYMENT GUIDE

## Why Fly.io?
- ✅ **ACTUALLY FREE** - 3 VMs included
- ✅ Different IP ranges (might work with Yahoo Finance)
- ✅ Global edge network
- ✅ Simple CLI deployment

---

## 📦 FILES NEEDED:

1. **bot_optimized.py** - Main bot
2. **scanner_yfinance.py** - Yahoo Finance scanner
3. **requirements.txt** - Dependencies
4. **fly.toml** - Fly.io configuration
5. **Dockerfile** - Container config (rename Dockerfile.fly to Dockerfile)

---

## 🚀 DEPLOYMENT STEPS:

### **Step 1: Install Fly CLI**

**Mac:**
```bash
brew install flyctl
```

**Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

**Windows:**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

---

### **Step 2: Sign Up & Login**

```bash
# Sign up (opens browser)
flyctl auth signup

# OR login if you have an account
flyctl auth login
```

**Free tier includes:**
- 3 shared-cpu VMs
- 256MB RAM each
- 160GB bandwidth/month
- **No credit card required!**

---

### **Step 3: Prepare Your Files**

```bash
# Navigate to your project folder
cd qullamaggie-bot

# Copy files from the zip
cp bot_optimized.py .
cp scanner_yfinance.py .
cp requirements.txt .
cp fly.toml .
cp Dockerfile.fly Dockerfile  # RENAME THIS!

# Verify files
ls -la
# Should show:
# - bot_optimized.py
# - scanner_yfinance.py
# - requirements.txt
# - fly.toml
# - Dockerfile
```

---

### **Step 4: Launch Your App**

```bash
# Create the app (from your project folder)
flyctl launch

# It will ask:
# "Would you like to copy its configuration to the new app?" 
# → Type: y (yes)

# "Do you want to tweak these settings before proceeding?"
# → Type: n (no)

# Fly will:
# 1. Create your app
# 2. Build the Docker image
# 3. Deploy to their edge network
```

---

### **Step 5: Watch Deployment**

```bash
# Watch logs in real-time
flyctl logs

# Expected output:
Scanner initialized with 50 Nasdaq stocks
Using Yahoo Finance (no API key needed)
Bot is ready with optimized concurrent scanning!
Application started
```

---

## 🧪 TESTING:

Once deployed, send `/scan` to your Telegram bot.

**If Yahoo Finance Works:**
```
🔍 Fetching NVDA...
✅ NVDA: $145.75 | Gap: +2.3% | Vol: 1.2x
✅ TSLA: $415.20 | Gap: +1.8% | Vol: 0.9x
[continues for 50 stocks...]
📊 Scan complete: 48 successful, 2 failed
🎯 Found 3 setups
```

**If Yahoo Finance is Blocked:**
```
Failed to get ticker 'NVDA' reason: Expecting value...
📊 Scan complete: 0 successful, 50 failed
```

---

## 📊 USEFUL FLY COMMANDS:

```bash
# View logs
flyctl logs

# Check app status
flyctl status

# SSH into your app
flyctl ssh console

# Restart app
flyctl apps restart qullamaggie-bot

# Stop app (saves resources)
flyctl scale count 0

# Start app again
flyctl scale count 1

# Destroy app
flyctl apps destroy qullamaggie-bot
```

---

## 🔧 IF YOU NEED TO UPDATE:

```bash
# After making code changes
flyctl deploy

# Force rebuild
flyctl deploy --no-cache
```

---

## 🎯 TROUBLESHOOTING:

### **Problem: "Not enough memory"**
```bash
# Increase to 512MB (still free tier)
flyctl scale memory 512
```

### **Problem: App keeps restarting**
```bash
# Check logs
flyctl logs

# Look for Python errors
```

### **Problem: Yahoo Finance still blocked**
Then we know Fly.io IPs are also blocked. Switch to Alpha Vantage:
- Add `ALPHA_VANTAGE_KEY` to fly.toml
- Use rate-limited scanner
- 6-minute scans but 100% reliable

---

## 💰 FREE TIER LIMITS:

| Resource | Free Tier |
|----------|-----------|
| **VMs** | 3 shared-cpu (256MB each) |
| **Bandwidth** | 160GB/month |
| **Storage** | 3GB persistent volumes |
| **Cost** | $0/month |

Your bot uses ~100MB RAM and minimal bandwidth = **Perfect for free tier!**

---

## 🌍 REGIONS:

Your bot is set to **"lhr" (London)** in fly.toml for low latency to UK.

Other options:
- `"lhr"` - London
- `"ams"` - Amsterdam  
- `"fra"` - Frankfurt
- `"cdg"` - Paris

---

## ✅ DEPLOYMENT CHECKLIST:

- [ ] Install Fly CLI
- [ ] Sign up / Login to Fly.io
- [ ] Copy 5 files to project folder
- [ ] Rename Dockerfile.fly to Dockerfile
- [ ] Run `flyctl launch`
- [ ] Watch logs with `flyctl logs`
- [ ] Test with `/scan` in Telegram

---

## 🎯 NEXT STEPS:

1. **Install Fly CLI** (takes 2 minutes)
2. **Sign up** (no credit card needed)
3. **Deploy** with `flyctl launch`
4. **Test** if Yahoo Finance works

If Yahoo works → **Problem solved!** ✅

If Yahoo is blocked → We use Alpha Vantage rate-limited (already have the code).

---

**Let's try Fly.io - it's actually free and might work with Yahoo Finance!** 🚀
