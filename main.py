# Imports
import os
import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message

def check(code) -> bool:
    for i in rest_commands:
        if code.count(i) > 0:
            return False
    return True
def err_message(code):
    for i in rest_commands:
        if code.count(i) > 0:
            return i
    return None


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv("CHANNEL")

async def send_message(message: str, channel: discord.TextChannel):
    await channel.send(message)


rest_commands = ["open(", "input(", "os", "pandas", "tkinter", "pygame", "winreg"]
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
            if check(code):
                with open("code.py", "w") as f:
                    f.write(code)
                os.system("code.py > output.txt")
            else:
                os.system(f"echo Your program cant use keyword {err_message(code)} > output.txt")
            with open("output.txt", "r") as f:
                output: str = f.read()
            final_output: str = f"```\n{output}```"
            await send_message(final_output, channel)


client.run(TOKEN)
