import discord
from discord.ext import tasks
import aiohttp
import asyncio
import json
import os
from datetime import datetime

# Load configuration from config.json
with open('config.json', 'r') as f:
    config = json.load(f)
    DISCORD_TOKEN = config['discord_token']
    CHANNEL_ID = config['channel_id']
    PRINTERS = config['printers']
    UPDATE_INTERVAL = config['update_interval']

class OctoPrintBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.channel = None

    async def setup_hook(self):
        self.update_status.start()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        self.channel = self.get_channel(int(CHANNEL_ID))
        # Delete previous messages from bot
        async for message in self.channel.history():
            if message.author == self.user:
                await message.delete()
        # Create initial messages for each printer
        for printer in PRINTERS:
            message = await self.channel.send(f"Initializing {printer['name']}... ({UPDATE_INTERVAL} sec~)")
            printer['message_id'] = message.id

    async def get_printer_status(self, printer):
        async with aiohttp.ClientSession() as session:
            headers = {'X-Api-Key': printer['api_key']}
            
            try:
                # Get printer state
                async with session.get(f"{printer['url']}/api/printer", headers=headers) as response:
                    if response.status == 200:
                        printer_data = await response.json()
                    else:
                        return f"Error: Cannot connect to {printer['name']}"

                # Get job state
                async with session.get(f"{printer['url']}/api/job", headers=headers) as response:
                    if response.status == 200:
                        job_data = await response.json()
                    else:
                        return f"Error: Cannot connect to {printer['name']}"

                # Format status message
                state = printer_data['state']['text']
                if state == "Printing":
                    completion = job_data['progress']['completion']
                    if completion is None:
                        completion = 0
                    time_left = job_data['progress']['printTimeLeft']
                    if time_left is None:
                        time_left = 0
                    
                    embed = discord.Embed(
                        title=printer['name'],
                        color=0x237DBD  # Same blue color as in the example
                    )
                    embed.add_field(name="Status", value=state, inline=True)
                    embed.add_field(name="Progress", value=f"{completion:.1f}%", inline=True)
                    embed.add_field(name="Time Remaining", value=f"{time_left // 60:.0f}m {time_left % 60:.0f}s", inline=True)
                    embed.add_field(name="File", value=job_data['job']['file']['name'], inline=False)
                    embed.set_footer(text=f"Last Updated - {datetime.now().strftime('%H:%M:%S')}")
                    
                    return {"embeds": [embed]}
                else:
                    embed = discord.Embed(
                        title=printer['name'],
                        color=0x237DBD
                    )
                    embed.add_field(name="Status", value=state, inline=True)
                    embed.set_footer(text=f"Last Updated - {datetime.now().strftime('%H:%M:%S')}")
                    
                    return {"embeds": [embed]}

            except Exception as e:
                return f"Error connecting to {printer['name']}: {str(e)}"



    @tasks.loop(seconds=UPDATE_INTERVAL)
    async def update_status(self):
        if not self.channel:
            return

        for printer in PRINTERS:
            if printer['message_id']:
                status = await self.get_printer_status(printer)
                message = await self.channel.fetch_message(printer['message_id'])
                await message.edit(content=status)

client = OctoPrintBot()
client.run(DISCORD_TOKEN)