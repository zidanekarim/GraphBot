import asyncio
import io
import os

import discord
import matplotlib.pyplot as plt
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=";", intents=intents, allowed_mentions=discord.AllowedMentions.none(),
                      activity=discord.Activity(
                          type=discord.ActivityType.listening,
                          name="Use $ for me!"),
                      status=discord.Status.online,)





@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have access to this command!")
    elif isinstance(error, commands.CommandOnCooldown):
        seconds = round(error.retry_after, 1)
        await ctx.send(f'Woah, slow down! Please wait `{seconds}` secs!')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You forgot a part of the command!')
    elif isinstance(error, commands.NotOwner):
        await ctx.send('You do not own this bot')
    elif isinstance(error, commands.PrivateMessageOnly):
        await ctx.send("You can only use this command in DMs! You are now dead")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Member not found!")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found!")
    elif isinstance(error, commands.ExtensionAlreadyLoaded):
        await ctx.send("Already on!")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Hey! You gave me a bad argument! How rude!!")
    else:
        raise error

   




@client.event
async def on_ready():
    print("Logged in")






@client.command(description='Loads extensions/cog. By default, all extensions are loaded', aliases=["enable", "on"])
@commands.has_permissions(administrator = True)
async def load(ctx, extension):
    """Load an extension! Admin only, by default all are loaded"""
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"Enabling {extension}!")


@load.error
async def load_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    await ctx.send("Something went wrong! You probably have this loaded already!")
    


@client.command(description="Disables an extension/cog. Usage - $unload extensionname", aliases=["disable", "off"])
@commands.has_permissions(administrator = True)
async def unload(ctx, extension):
  """Disables an extension/cog. Usage - $unload extensionname"""
  client.unload_extension(f'cogs.{extension}')
  await ctx.send(f"Disabling {extension}!")

@client.command(description="Reloads an extension/cog in case of code update. Usage- $reload extensionname")
@commands.has_permissions(administrator = True)
async def reload(ctx, extension):
  """Reload an extension"""
  client.reload_extension(f'cogs.{extension}')
  await ctx.send(f"Reloading {extension}!")



for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')




client.run(os.getenv("TOKEN"))

