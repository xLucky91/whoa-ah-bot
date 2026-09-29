import discord
import os
import json
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def load_punkte():
    if not os.path.exists("punkte.json"):
        return {}
    with open("punkte.json", "r") as f:
        try:
            data = f.read()
            if not data:
                return {}
            return json.loads(data)
        except:
            return {}

def save_punkte(data):
    with open("punkte.json", "w") as f:
        json.dump(data, f)

class VoteView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    @discord.ui.button(label="Geil", style=discord.ButtonStyle.green, emoji="🔥")
    async def geil(self, interaction, button):
        p = load_punkte()
        uid = str(self.user_id)
        p[uid] = p.get(uid, 0) + 1
        save_punkte(p)
        await interaction.response.send_message(f"+1 | Du hast jetzt {p[uid]} Punkte", ephemeral=True)

    @discord.ui.button(label="Schrott", style=discord.ButtonStyle.red, emoji="💩")
    async def schrott(self, interaction, button):
        p = load_punkte()
        uid = str(self.user_id)
        p[uid] = p.get(uid, 0) - 1
        save_punkte(p)
        await interaction.response.send_message(f"-1 | Du hast jetzt {p[uid]} Punkte", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Online als {bot.user} - Bot laeuft!")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! Bot laeuft!")

@bot.command()
async def top(ctx):
    p = load_punkte()
    if not p:
        await ctx.send("Noch keine Punkte")
        return
    sortiert = sorted(p.items(), key=lambda x: x[1], reverse=True)[:10]
    text = "**Top Loot Hunter:**\n"
    for i, (uid, pts) in enumerate(sortiert, 1):
        text += f"{i}. <@{uid}> - {pts} Punkte\n"
    await ctx.send(text)

@bot.event
async def on_message(msg):
    if msg.author.bot:
        return
    if msg.attachments:
        for a in msg.attachments:
            if a.content_type and "image" in a.content_type:
                embed = discord.Embed(title="WoA Drop", description=f"Von {msg.author.mention}", color=discord.Color.gold())
                embed.set_image(url=a.url)
                await msg.channel.send(embed=embed, view=VoteView(msg.author.id))
    await bot.process_commands(msg)

token = os.getenv("DISCORD_TOKEN")
if token:
    bot.run(token)
