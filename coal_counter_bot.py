import logging
import requests
import time
from telegram import Bot
from telegram.constants import ParseMode

# Config
BOT_TOKEN = '8261654850:AAH49Ees9Fm4Sr0AhNI0JXF7dBnW200n7o0'  # From @BotFather
CHAT_ID = '-1003132385064'  # Your group
CONTRACT_ADDRESS = '0xD0Dce4A1aC8D6195a9628800cE518e278808d11a'
TARGET_MC = 30000
TARGET_VOL = 20000  # Daily vol goal
TARGET_LIQ = 20000  # Liq goal
MC_THRESHOLD = 1000
VOL_THRESHOLD = 500
LIQ_THRESHOLD = 1000
POLL_INTERVAL = 30  # Seconds

bot = Bot(token=BOT_TOKEN)
message_id = None  # Persistent msg ID
last_mc = last_vol = last_liq = None

logging.basicConfig(level=logging.INFO)

def get_current_stats():
    """Fetch current MC, Volume, and Liquidity from DexScreener API"""
    global last_mc, last_vol, last_liq
    try:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{CONTRACT_ADDRESS}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        
        if data.get('pairs') and len(data['pairs']) > 0:
            # Find Base pair or default to first
            pair = next((p for p in data['pairs'] if p.get('chainId') == 'base'), data['pairs'][0])
            
            mc = float(pair.get('marketCap', 0) or pair.get('fdv', 0))
            vol = float(pair.get('volume', {}).get('h24', 0))
            liq = float(pair.get('liquidity', {}).get('usd', 0))
            
            return mc, vol, liq
        
        return None, None, None
    except Exception as e:
        logging.error(f"Stats fetch failed: {e}")
        return last_mc, last_vol, last_liq  # Fallback

def generate_mini_bar(current_percent, emoji='█'):
    """Generate a visual progress bar with emoji"""
    filled = int(current_percent / 10)  # 10 blocks
    bar = f"{emoji * filled}{'░' * (10 - filled)} {current_percent:.0f}%"
    return bar

def send_or_edit_message(mc, vol, liq):
    """Send initial message or edit existing one"""
    global message_id
    
    mc_pct = min((mc / TARGET_MC) * 100, 100)
    vol_pct = min((vol / TARGET_VOL) * 100, 100)
    liq_pct = min((liq / TARGET_LIQ) * 100, 100)
    
    mc_bar = generate_mini_bar(mc_pct, '🎄')
    vol_bar = generate_mini_bar(vol_pct, '🔥')
    liq_bar = generate_mini_bar(liq_pct, '💧')
    
    text = f"""*Holi\\-Daze $HOLI Tracker 🚀🎄*

*MC to 30K:*
{mc_bar}
${mc:,.0f} / ${TARGET_MC:,} 🎁

*Vol 24h to 20K:*
{vol_bar}
${vol:,.0f} / ${TARGET_VOL:,} 🔥

*Liq to 20K:*
{liq_bar}
${liq:,.0f} / ${TARGET_LIQ:,} 💧

Diamond hands or coal? Ape: t\\.me/baseholidaze
CA: `{CONTRACT_ADDRESS}`

\\#HoliDaze \\#BaseMas 🐒
"""
    
    try:
        if message_id is None:
            msg = bot.send_message(
                chat_id=CHAT_ID, 
                text=text.strip(), 
                parse_mode=ParseMode.MARKDOWN_V2
            )
            message_id = msg.message_id
            logging.info(f"Initial msg: MC ${mc:,.0f}, Vol ${vol:,.0f}, Liq ${liq:,.0f}")
        else:
            bot.edit_message_text(
                chat_id=CHAT_ID, 
                message_id=message_id, 
                text=text.strip(), 
                parse_mode=ParseMode.MARKDOWN_V2
            )
            logging.info(f"Updated: MC ${mc:,.0f}, Vol ${vol:,.0f}, Liq ${liq:,.0f}")
    except Exception as e:
        logging.error(f"Message send/edit failed: {e}")

def main():
    """Main bot loop"""
    global last_mc, last_vol, last_liq
    
    logging.info("CoalCounterBot starting... 🎄")
    
    while True:
        try:
            mc, vol, liq = get_current_stats()
            
            if mc is None:
                logging.warning("No data received, retrying...")
                time.sleep(POLL_INTERVAL)
                continue
            
            trigger = False
            if last_mc is not None:
                # Check if any metric changed significantly
                if (abs(mc - last_mc) >= MC_THRESHOLD or 
                    abs(vol - last_vol) >= VOL_THRESHOLD or 
                    abs(liq - last_liq) >= LIQ_THRESHOLD):
                    trigger = True
            else:
                trigger = True  # Initial send
            
            if trigger:
                send_or_edit_message(mc, vol, liq)
            
            last_mc, last_vol, last_liq = mc, vol, liq
            time.sleep(POLL_INTERVAL)
            
        except KeyboardInterrupt:
            logging.info("Bot stopped by user")
            break
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
