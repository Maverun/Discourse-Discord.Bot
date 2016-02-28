from discord.ext import commands
from Cogs.Utils import Read
import datetime
import glob

Config=Read.config
description = '''{} bot Command List. '''.format(Config["Bot name"])
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in')
    print(bot.user.id)
    print('------')
    bot.uptime = datetime.datetime.utcnow()
    load_cogs()


def get_bot_uptime():
    now = datetime.datetime.utcnow()
    delta = now - bot.uptime
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if days:
        fmt = '**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds'
    else:
        fmt = '**{h}** hours, **{m}** minutes, and **{s}** seconds'

    return fmt.format(d=days, h=hours, m=minutes, s=seconds)

@bot.command()
async def uptime(): #Showing Time that bot been total run
    """Tells you how long the bot has been up for."""
    await bot.say('I been up for {}'.format(get_bot_uptime()))

def load_cogs():
    cogs = list_cogs()
    for cogs in cogs:
        print (cogs)
        try:
            bot.load_extension(cogs)
            print ("Load {}".format(cogs))
        except Exception as e:
            print(e)

def list_cogs():
    cogs = glob.glob("Cogs/*.py")
    clean = []
    for c in cogs:
        c = c.replace("/", "\\") # Linux fix
        clean.append("Cogs." + c.split("\\")[1].replace(".py", ""))
    return clean

if __name__ == '__main__':
    bot.run(Config['username'], Config['password'])
