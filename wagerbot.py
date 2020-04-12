from OAuth2Info import *
import discord
from discord.ext import commands
import random

openwagers = {}
confirmedwagers = {}
wagersloss = {}
wagerswon = {}
settings = {
  "userlimit": 0,  # 0 = Everyone can play, 1 = subscribed only, 2 = only mods can play
  "minbet": "20",
  "currency": "USD"
}
description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    #print(bot.user.id)
    print('------')
@bot.event
async def event_message(ctx):
    if ctx.author.name.lower() == bot.user.name:
        return
    print(f'{ctx.channel} - {ctx.author.name}: {ctx.content}')

@bot.command(name='wager')
async def wager(ctx, arg1 = "NULL"):
    global openwagers
    global settings
    if arg1.isdigit():
        if ctx.author.name in openwagers:
            openwagers[ctx.author.name] = str(int(openwagers[ctx.author.name]) + int(arg1))
            await ctx.channel.send(
                f"{ctx.author.name} adding another {arg1} to their open wager for a total of {openwagers[ctx.author.name]} ! If this is too much for you please use the !wager remove command.")
        else:
            await ctx.channel.send(f"{ctx.author.name} wants to wager {arg1} !")
            openwagers[ctx.author.name] = arg1
    elif arg1 == 'remove':
        del openwagers[ctx.author.name]
        await ctx.channel.send(f"{ctx.author.name} removed their wager!")
    else:
        await ctx.channel.send(
            f"{ctx.author.name} to wager you need to show intent by typing !wager XX where XX is a number representing how much {settings['currency']} you want to wager. {settings['minbet']}{settings['currency']} minimum! Use !wager remove to remove your unbooked bet.  Once booked you are locked in unless the bookie says.")

@bot.command(name='bookie')
async def bookie(ctx, arg1 = "NULL", arg2 = "NULL"):
    global bookiename
    if ctx.author.name == bookiename:
        global openwagers
        global confirmedwagers
        global wagerswon
        global wagersloss
        global settings
        #list all users who want to wager
        if arg1 == "$":
            await ctx.channel.send(f"Open bets {openwagers} confirmed bets {confirmedwagers} the bookie has won {wagerswon} and the bookie has loss {wagersloss} ")
        #book/confirm wager
        elif arg1 == 'bet':
            if arg2 in confirmedwagers:
                confirmedwagers[arg2] = str(int(openwagers[arg2]) + int(confirmedwagers[arg2]))
                del openwagers[arg2]
                await ctx.channel.send(f"{arg2} your bet for {confirmedwagers[arg2]} is locked in!")
            else:
                confirmedwagers[arg2] = openwagers[arg2]
                del openwagers[arg2]
                await ctx.channel.send(f"{arg2} your bet for {confirmedwagers[arg2]} is locked in!")
        #remove confirmed wager
        elif arg1 == 'remove':
            del confirmedwagers[arg2]
            await ctx.channel.send(f"The bookie has removed the wager for {arg2} ")
        elif arg1 == 'won':
            if arg2 in wagerswon:
                wagerswon[arg2] = str(int(confirmedwagers[arg2]) + int(wagerswon[arg2]))
                del confirmedwagers[arg2]
                await ctx.channel.send(f"You loss to the bookie {arg2} .")
            else:
                wagerswon[arg2] = confirmedwagers[arg2]
                del confirmedwagers[arg2]
                await ctx.channel.send(f"You loss {wagerswon[arg2]} to the bookie {arg2} .")
        elif arg1 == 'loss':
            if arg2 in wagersloss:
                wagersloss[arg2] = str(int(confirmedwagers[arg2]) + int(wagersloss[arg2]))
                del confirmedwagers[arg2]
                await ctx.channel.send(f"You beat the bookie {arg2} for {wagersloss[arg2]} .")
            else:
                wagersloss[arg2] = confirmedwagers[arg2]
                del confirmedwagers[arg2]
                await ctx.channel.send(f"You beat the bookie {arg2} .")
        elif arg1 == 'newbookie':
            bookiename = arg2
            await ctx.channel.send(f"New bookie is {arg2} ")
        elif arg1 == 'delopen':
            openwagers = {}
            await ctx.channel.send(f"All open wagers have been removed")
        elif arg1 == 'reset':
            openwagers = {}
            confirmedwagers = {}
            wagersloss = {}
            wagerswon = {}
            await ctx.channel.send(f"WagerBot has been reset")
        elif arg1 == "mode":
            if arg2 == "mods":
                settings["userlimit"] = 2
                await ctx.channel.send(f"Wagers limited to mods only.")
            elif arg2 == "subs":
                settings["userlimit"] = 1
                await ctx.channel.send(f"Wagers limited to subscribers only.")
            elif arg2 == "all":
                settings["userlimit"] = 0
                await ctx.channel.send(f"Wagers open for everyone!")
        else:
            await ctx.channel.send(f"{ctx.author.name} to book a wager you need to confirm intent by typing !bookie bet NameOfPersonWagering or use !bookie # to list all wagers. Using !bookie won/loss NameOfPerson will move them to the won/loss against the bookie categories. !bookie delopen removes all open wagers. bookie reset will reset everything.")
    else:
       await ctx.channel.send(f"{ctx.author.name} you are not set as the bookie")

bot.run(OTOKEN)
