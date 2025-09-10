
```python
import os
import aiohttp
import asyncio
from discord import Client, Intents
from discord.ext.tasks import loop
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

file_name = "target_price.txt"
intents = Intents.default()
intents.message_content = True
bot = Client(intents=intents)

alerts_enabled = True
alert_interval = 10  # seconds

def get_target_price():
    try:
        with open(file_name) as f:
            target_price = f.read().strip()
        return float(target_price) if target_price else 0.0
    except FileNotFoundError:
        return 0.0

def set_target_price(new_target_price):
    with open(file_name, 'w') as f:
        f.write(str(float(new_target_price)))

async def get_change(interval: str):
    url_stats = "https://api.kucoin.com/api/v1/market/stats?symbol=BTC-EUR"
    if interval == "24h":
        async with aiohttp.ClientSession() as session:
            async with session.get(url_stats) as resp:
                data = await resp.json()
                stats = data.get("data", {})
                change_price = float(stats.get("changePrice", 0))
                change_rate = float(stats.get("changeRate", 0)) * 100
                return f"In the last 24h: {change_price:.2f} EUR ({change_rate:.2f}%)"

    mapping = {
        "1h": ("1hour", 3600),
        "6h": ("1hour", 3600*6),
        "12h": ("1hour", 3600*12),
        "7d": ("1day", 86400*7),
    }
    if interval not in mapping:
        return "Invalid interval. Use 24h, 1h, 6h, 12h, or 7d."

    ktype, seconds = mapping[interval]
    now = int(aiohttp.helpers._current_time())
    start = now - seconds
    candles_url = f"https://api.kucoin.com/api/v1/market/candles?symbol=BTC-EUR&type={ktype}&startAt={start}&endAt={now}"

    async with aiohttp.ClientSession() as session:
        async with session.get(candles_url) as resp:
            data = await resp.json()
            candles = data.get("data", [])
            if not candles:
                return "Could not fetch candle data."
            candles_sorted = sorted(candles, key=lambda c: int(c[0]))
            p0 = float(candles_sorted[0][1])
            p1 = float(candles_sorted[-1][2])
            change_price = p1 - p0
            change_rate = (change_price / p0) * 100
            return f"In the last {interval}: {change_price:.2f} EUR ({change_rate:.2f}%)"

@bot.event
async def on_ready():
    send_quotation.start()

@loop(seconds=alert_interval)
async def send_quotation():
    global alerts_enabled
    if not alerts_enabled:
        return

    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.kucoin.com/api/v1/market/stats?symbol=BTC-EUR") as response:
            data = await response.json()
            actual_price = float(data["data"]["buy"])

    channel = bot.get_channel(CHANNEL_ID)
    if actual_price < get_target_price():
        await channel.send(f"Current BTC price: {actual_price:.2f} EUR")
        await channel.send("It is time to buy!")

@bot.event
async def on_message(message):
    global alerts_enabled, alert_interval
    if message.author == bot.user:
        return

    content = (message.content or "").strip()
    if not content:
        return

    parts = content.split()
    cmd = parts[0].lower()
    channel = message.channel

    if cmd == "!alerts":
        arg = parts[1].lower() if len(parts) > 1 else None
        if arg == "off":
            alerts_enabled = False
            await channel.send("Alerts disabled.")
        elif arg == "on":
            alerts_enabled = True
            await channel.send("Alerts enabled.")
        else:
            await channel.send("Use `!alerts on` or `!alerts off`.")
        return

    if cmd == "!target_price":
        if len(parts) > 1:
            try:
                new_target = float(parts[1])
                set_target_price(new_target)
                await channel.send(f"New target price set to {new_target:.2f} EUR")
            except ValueError:
                await channel.send("Please provide a valid number.")
        else:
            await channel.send("Usage: !target_price <new target price>")
        return

    if cmd == "!btc":
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.kucoin.com/api/v1/market/stats?symbol=BTC-EUR") as response:
                data = await response.json()
                price = float(data["data"]["buy"])
                await channel.send(f"Current BTC price: {price:.2f} EUR")
        return

    if cmd == "!alert_time":
        if len(parts) > 1:
            try:
                interval = int(parts[1])
                alert_interval = interval
                send_quotation.change_interval(seconds=alert_interval)
                await channel.send(f"Alert interval set to {alert_interval} seconds.")
            except ValueError:
                await channel.send("Please provide a valid number of seconds.")
        else:
            await channel.send("Usage: !alert_time <seconds>")
        return

    if cmd == "!change":
        if len(parts) > 1:
            interval = parts[1].lower()
            msg = await get_change(interval)
            await channel.send(msg)
        else:
            await channel.send("Usage:

