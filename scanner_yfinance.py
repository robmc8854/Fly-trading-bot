"""
QULLAMAGGIE SCANNER - YAHOO FINANCE
No API keys, no rate limits, works immediately
"""

import yfinance as yf
import asyncio
from typing import List, Dict
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class QullamaggieScanner:
    def __init__(self):
        # Top 50 Nasdaq stocks by volume and momentum
        self.nasdaq_stocks = [
            # Mega caps
            'NVDA', 'TSLA', 'META', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'NFLX',
            
            # High momentum
            'SMCI', 'ARM', 'PLTR', 'COIN', 'MSTR', 'AVGO', 'AMD', 'TSM',
            
            # Recent movers
            'CRWD', 'SNOW', 'DDOG', 'NET', 'ROKU', 'RIVN', 'LCID', 'UBER',
            
            # Semiconductors
            'ASML', 'QCOM', 'AMAT', 'LRCX', 'KLAC', 'SNPS', 'CDNS',
            
            # Software/Cloud  
            'CRM', 'ORCL', 'ADBE', 'INTU', 'NOW', 'PANW', 'WDAY',
            
            # China/EV
            'NIO', 'XPEV', 'LI', 'BABA', 'PDD', 'JD',
            
            # Other high-volume
            'DASH', 'ABNB', 'HOOD', 'RBLX', 'PINS', 'SPOT'
        ]
        
        logger.info(f"Scanner initialized with {len(self.nasdaq_stocks)} Nasdaq stocks")
        logger.info("Using Yahoo Finance (no API key needed)")
        
    def get_stock_data(self, symbol: str) -> Dict:
        """Get stock data from Yahoo Finance"""
        try:
            logger.info(f"🔍 Fetching {symbol}...")
            
            # Download last 30 days of data
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='1mo')
            
            if hist.empty or len(hist) < 2:
                logger.warning(f"{symbol}: No data available")
                return None
            
            # Get last 2 days
            current = hist.iloc[-1]
            previous = hist.iloc[-2]
            
            # Calculate 20-day average volume
            avg_volume = hist['Volume'].tail(20).mean() if len(hist) >= 20 else hist['Volume'].mean()
            
            # Calculate metrics
            current_price = float(current['Close'])
            prev_close = float(previous['Close'])
            gap_pct = ((current_price - prev_close) / prev_close) * 100
            volume_ratio = float(current['Volume']) / avg_volume if avg_volume > 0 else 0
            
            result = {
                'symbol': symbol,
                'current_price': current_price,
                'prev_close': prev_close,
                'high': float(current['High']),
                'low': float(current['Low']),
                'open': float(current['Open']),
                'volume': float(current['Volume']),
                'avg_volume': avg_volume,
                'date': current.name.strftime('%Y-%m-%d'),
            }
            
            logger.info(f"✅ {symbol}: ${current_price:.2f} | Gap: {gap_pct:+.1f}% | Vol: {volume_ratio:.1f}x")
            return result
            
        except Exception as e:
            logger.error(f"{symbol}: Error - {e}")
            return None
    
    async def scan_all_stocks(self) -> List[Dict]:
        """Scan all stocks (Yahoo Finance is fast, no rate limits)"""
        setups = []
        successful = 0
        failed = 0
        
        logger.info(f"🚀 Starting scan of {len(self.nasdaq_stocks)} stocks...")
        
        for symbol in self.nasdaq_stocks:
            data = await asyncio.to_thread(self.get_stock_data, symbol)
            
            if data:
                successful += 1
                
                # Calculate metrics
                gap_pct = ((data['current_price'] - data['prev_close']) / data['prev_close']) * 100
                volume_ratio = data['volume'] / data['avg_volume'] if data['avg_volume'] > 0 else 0
                
                # EPISODIC PIVOT
                if gap_pct >= 8.0 and volume_ratio >= 2.0:
                    entry_price = data['high']
                    stop_price = data['low']
                    risk_pct = ((entry_price - stop_price) / entry_price) * 100
                    
                    if risk_pct <= 12.0:
                        score = 70 + min(20, int(gap_pct)) + min(10, int(volume_ratio))
                        
                        setup = {
                            'symbol': data['symbol'],
                            'type': 'EPISODIC PIVOT',
                            'score': min(100, score),
                            'rating': 3 if score >= 85 else 2,
                            'entry': entry_price,
                            'stop': stop_price,
                            'risk_pct': risk_pct,
                            'catalyst': f"Gap +{gap_pct:.1f}% on {volume_ratio:.1f}x volume",
                        }
                        setups.append(setup)
                        logger.info(f"🎯 EPISODIC PIVOT: {data['symbol']} - Gap +{gap_pct:.1f}%")
                
                # BREAKOUT
                elif gap_pct >= 3.0 and volume_ratio >= 1.5:
                    entry_price = data['current_price'] * 1.01
                    stop_price = data['low']
                    risk_pct = ((entry_price - stop_price) / entry_price) * 100
                    
                    if risk_pct <= 8.0:
                        score = 75 + min(15, int(gap_pct)) + min(10, int(volume_ratio))
                        
                        setup = {
                            'symbol': data['symbol'],
                            'type': 'BREAKOUT',
                            'score': min(100, score),
                            'rating': 2,
                            'entry': entry_price,
                            'stop': stop_price,
                            'risk_pct': risk_pct,
                            'catalyst': f"Move +{gap_pct:.1f}% on {volume_ratio:.1f}x vol",
                        }
                        setups.append(setup)
                        logger.info(f"📈 BREAKOUT: {data['symbol']} - Move +{gap_pct:.1f}%")
                
                # VOLUME SURGE
                elif volume_ratio >= 3.0 and gap_pct >= 1.0:
                    entry_price = data['current_price'] * 1.005
                    stop_price = data['low']
                    risk_pct = ((entry_price - stop_price) / entry_price) * 100
                    
                    if risk_pct <= 6.0:
                        score = 65 + min(10, int(volume_ratio)) + min(5, int(gap_pct))
                        
                        setup = {
                            'symbol': data['symbol'],
                            'type': 'VOLUME SURGE',
                            'score': min(100, score),
                            'rating': 2,
                            'entry': entry_price,
                            'stop': stop_price,
                            'risk_pct': risk_pct,
                            'catalyst': f"Volume {volume_ratio:.1f}x with +{gap_pct:.1f}%",
                        }
                        setups.append(setup)
                        logger.info(f"🔊 VOLUME SURGE: {data['symbol']}")
            else:
                failed += 1
        
        logger.info("=" * 60)
        logger.info(f"📊 Scan complete: {successful} successful, {failed} failed")
        logger.info(f"🎯 Found {len(setups)} setups")
        logger.info("=" * 60)
        
        return sorted(setups, key=lambda x: x['score'], reverse=True)
    
    async def scan_all(self) -> List[Dict]:
        """Main scan entry point"""
        logger.info("=" * 60)
        logger.info("QULLAMAGGIE SCANNER - YAHOO FINANCE")
        logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        setups = await self.scan_all_stocks()
        
        if setups:
            logger.info(f"✅ Found {len(setups)} qualifying setups!")
            return setups[:5]
        else:
            logger.info("📊 No qualifying setups found")
            return [{
                'symbol': 'NO_SETUPS',
                'type': 'MARKET SCAN COMPLETE',
                'score': 0,
                'rating': 0,
                'entry': 0,
                'stop': 0,
                'risk_pct': 0,
                'catalyst': f'Scanned {len(self.nasdaq_stocks)} stocks - no qualifying setups. Market may be consolidating.',
            }]
