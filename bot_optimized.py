"""
QULLAMAGGIE TELEGRAM BOT - OPTIMIZED VERSION
Fast concurrent scanning with Alpha Vantage API
"""

import os
import logging
from datetime import datetime, time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

# Import Yahoo Finance scanner
from scanner_yfinance import QullamaggieScanner

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '8272225940:AAGhXTu3eit5m9Bh7EdO7DYlvWTbFnhrmu4')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '688830637')
TESTING_MODE = os.getenv('TESTING_MODE', 'True').lower() == 'true'
ACCOUNT_SIZE = float(os.getenv('ACCOUNT_SIZE', '100000'))
ALPHA_VANTAGE_KEY = os.getenv('ALPHA_VANTAGE_KEY', 'demo')

# UK timezone
UK_TZ = pytz.timezone('Europe/London')

class QullamaggieBot:
    def __init__(self):
        self.scanner = QullamaggieScanner()
        self.scheduler = AsyncIOScheduler(timezone=UK_TZ)
        self.application = None
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command"""
        welcome_msg = f"""
🎯 **QULLAMAGGIE BOT - YAHOO FINANCE**

{"📋 **TEST MODE**" if TESTING_MODE else "💰 **LIVE MODE**"}

**Configuration:**
• Account: £{ACCOUNT_SIZE:,.0f}
• Data Source: Yahoo Finance (FREE!)
• Stocks Scanned: 50 high-volume Nasdaq
• Scan Speed: ⚡ 30-60 seconds

**What I Scan:**
• Full Nasdaq (NVDA, TSLA, AAPL, SMCI, etc.)
• Real gaps and volume data
• Live market conditions

**Commands:**
/scan - Scan for REAL setups now
/help - Full command list

**Status:** ✅ Ready to scan! No API key needed!

Ready to find REAL Qullamaggie setups! 🚀
        """
        await update.message.reply_text(welcome_msg, parse_mode='Markdown')
        
    async def scan_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manual scan command - OPTIMIZED"""
        logger.info(f"Scan command received from user {update.effective_user.id}")
        
        await update.message.reply_text("🔍 **Scanning 50 Nasdaq stocks with Yahoo Finance...**\n⚡ This will take 30-60 seconds", parse_mode='Markdown')
        
        try:
            # Run the optimized scanner
            setups = await self.scanner.scan_all()
            
            if not setups:
                await update.message.reply_text("No qualifying setups found in current market conditions.")
                return
                
            # Format and send results
            message = self._format_scan_results(setups)
            await update.message.reply_text(message, parse_mode='Markdown', disable_web_page_preview=True)
            logger.info(f"Scan complete: {len(setups)} setups found")
            
        except Exception as e:
            logger.error(f"Error in scan: {e}", exc_info=True)
            await update.message.reply_text(f"⚠️ Scan error: {str(e)}")
        
    def _format_scan_results(self, setups):
        """Format scan results with TradingView links"""
        if not setups:
            return "No setups found."
            
        message = "🎯 **SCAN RESULTS:**\n\n"
        
        for setup in setups[:5]:
            stars = "⭐" * setup['rating']
            chart_link = f"https://www.tradingview.com/chart/?symbol=NASDAQ:{setup['symbol']}"
            
            # Handle special setup types
            if setup['symbol'] in ['SETUP_REQUIRED', 'NO_SETUPS', 'API_KEY_NEEDED']:
                message += f"""
{stars} **{setup['symbol']} - {setup['type']}**

{setup['catalyst']}

📊 [View Chart]({chart_link})

---
"""
            else:
                message += f"""
{stars} **{setup['symbol']} - {setup['type']}**

• Entry: £{setup['entry']:.2f}
• Stop: £{setup['stop']:.2f}
• Risk: {setup['risk_pct']:.1f}%
• Score: {setup['score']}/100

{setup['catalyst']}

📊 [View Chart]({chart_link})

---
"""
        return message.strip()
        
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help"""
        api_status = "✅ Real data" if ALPHA_VANTAGE_KEY != 'demo' else "⚠️ Demo mode"
        
        help_text = f"""
📚 **QULLAMAGGIE BOT - OPTIMIZED**

**Status:** {api_status}

**Main Commands:**
/scan - Fast scan (30-60 seconds)
/start - Bot info and status
/help - This message

**What I Do:**
✅ Scan 30 high-priority Nasdaq stocks
✅ Find real Episodic Pivots (8%+ gaps)
✅ Find real Breakouts (volume + momentum)
✅ Use concurrent API calls (FAST!)
✅ Apply exact Qullamaggie rules

**Optimizations:**
⚡ Concurrent requests (not sequential)
⚡ Focused on high-momentum stocks
⚡ Smart rate limiting
⚡ 30-60 second response time

**Setup:**
{"✅ Alpha Vantage API connected" if ALPHA_VANTAGE_KEY != 'demo' else "⚠️ Get free API key: https://www.alphavantage.co/support/#api-key"}

Ready to scan! 🎯
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
        
    async def send_message(self, text):
        """Send message to Telegram"""
        try:
            await self.application.bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=text,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            
    async def daily_scan(self):
        """Scheduled daily scan"""
        logger.info("Running scheduled daily scan...")
        try:
            setups = await self.scanner.scan_all()
            
            if setups and setups[0]['symbol'] not in ['SETUP_REQUIRED', 'NO_SETUPS']:
                message = "🌅 **DAILY SCAN RESULTS**\n\n"
                message += self._format_scan_results(setups)
                await self.send_message(message)
            elif setups and setups[0]['symbol'] == 'NO_SETUPS':
                await self.send_message("📊 **Daily Scan:** No qualifying setups in current market conditions.")
            else:
                await self.send_message("📊 **Daily Scan:** API setup required for real data scanning.")
        except Exception as e:
            logger.error(f"Error in daily scan: {e}")
            
    def setup_scheduler(self):
        """Setup scheduled jobs"""
        # Daily scan at 12:00 PM UK
        self.scheduler.add_job(
            self.daily_scan,
            CronTrigger(hour=12, minute=0, timezone=UK_TZ),
            id='daily_scan'
        )
        
        self.scheduler.start()
        logger.info("Scheduler started - daily scan at 12 PM UK")
        
    def run(self):
        """Start the bot"""
        logger.info("Starting Qullamaggie Bot - OPTIMIZED VERSION...")
        logger.info(f"API Key: {'Configured' if ALPHA_VANTAGE_KEY != 'demo' else 'Not set (demo mode)'}")
        
        # Create application
        self.application = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # Add command handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("scan", self.scan_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        # Setup scheduler
        self.setup_scheduler()
        
        logger.info("Bot is ready with optimized concurrent scanning!")
        self.application.run_polling()

if __name__ == '__main__':
    bot = QullamaggieBot()
    bot.run()
