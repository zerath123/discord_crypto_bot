# Discord Crypto Bot

A real-time cryptocurrency tracking bot for Discord, built with Python and the KuCoin API.  
Monitor Bitcoin (BTC) prices, set alerts for target prices, check price changes over different intervals, and stay updated directly in your Discord server.

---

## Features

- Track the current price of Bitcoin (BTC) and other cryptocurrencies.
- Set a target price and receive alerts when the price goes above or below it.
- Enable or disable alerts at any time.
- Customize the interval between alerts.
- Check price differences over different intervals (1h, 6h, 12h, 24h, 7d).
- View the current BTC price and your target price.
- Easily extendable to support additional cryptocurrencies.

---

## Commands

| Command | Description |
|---------|-------------|
| `!target_price <new target price>` | Set or modify your desired target price for BTC. |
| `!alerts on/off` | Enable or disable target price alerts. |
| `!btc` | Show the current price of 1 BTC even if alerts are disabled. |
| `!alert_time <seconds>` | Change the interval between price alerts. |
| `!change <interval>` | Show the price difference for a selected interval (`1h`, `6h`, `12h`, `24h`, `7d`). |
| `!actual_target` | Show the current BTC price and your target price. |

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/discord_crypto_bot.git
cd discord_crypto_bot

Install dependencies, configure environment, set the initial target price, and run the bot:
bash
pip install -r requirements.txt

# Create a .env file based on .env.example
# and add your Discord bot token and channel ID
# Example content of .env:
# DISCORD_TOKEN=your_discord_bot_token
# CHANNEL_ID=your_discord_channel_id

# Create a file named target_price.txt with your initial target price
# Example content:
# 100000

# Run the bot
python discord_bot.py

Notes

Alerts only work while the bot is running.

You can extend the bot to track multiple cryptocurrencies by modifying the !price command and saving separate target prices.

Keep your .env file private and never push it to GitHub.

Requirements

Python 3.10+

Libraries:

pip install discord.py aiohttp python-dotenv requests

License

Open-source and free to use.
