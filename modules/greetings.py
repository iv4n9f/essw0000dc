import discord
from discord.ext import commands

def setup(bot):
    @bot.command()
    async def hello(ctx, name: str):
        embed = discord.Embed(
            title="👋 Greeting",
            description=f"Hello, **{name}**! Welcome! 😊",
            color=discord.Color.blue()  # Puedes cambiar el color
        )
        embed.set_footer(text="Nexus Server")
        await ctx.send(embed=embed)
