# Imports
import os
import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv("CHANNEL")

async def send_message(message: str, channel: discord.TextChannel):
    await channel.send(message)


# Setup
intents: Intents = Intents.default()
intents.message_content = True  # NOQA

client: Client = Client(intents=intents)


# StartUp
@client.event
async def on_ready() -> None:
    print(f"{client.user} is now online!")


@client.event
async def on_message(message: Message) -> None:
    username: str = str(message.author)
    content: str = message.content
    channel = message.channel
    if message.author == client.user:
        return
    if str(channel) == CHANNEL and content.count("```") == 2:
        lang: str = content.split("```")[1].split("\n")[0]
        code: str = "\n".join(content.split("```")[1].split("\n")[1:])
        if lang == "python":
            with open("code.py", "w") as f:
                f.write(code)
            os.system("code.py > output.txt")
            with open("output.txt", "r") as f:
                output: str = f.read()
            final_output: str = f"```\n{output}```"
            await send_message(final_output, channel)


client.run(TOKEN)
