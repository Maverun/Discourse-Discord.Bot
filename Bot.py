from discord.ext import commands
from Cogs.Utils import Read
import datetime
import glob

Main_Config=Read.config
description = '''{} bot Command List. '''.format(Main_Config["Bot name"])
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in')
    print(bot.user.id)
    print('------')
    bot.uptime = datetime.datetime.utcnow()
<<<<<<< HEAD
    load_cogs()

=======
    global Data_channel
    Data_channel = bot.get_channel(Main_Config["Data Channel"])
    bot.loop.create_task(fetch_latest_in_background())

async def fetch_latest_in_background():
    try:
        await latest()
    finally:
        bot.loop.call_later(Main_Config["Second"], lambda: bot.loop.create_task(fetch_latest_in_background()))
>>>>>>> origin/master

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

<<<<<<< HEAD
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
    cogs = glob.glob("cogs/*.py")
    clean = []
    for c in cogs:
        c = c.replace("/", "\\") # Linux fix
        clean.append("cogs." + c.split("\\")[1].replace(".py", ""))
    return clean

if __name__ == '__main__':
    bot.run(Main_Config['username'], Main_Config['password'])
=======
@bot.command(name = "time",brief="Allow to change timer for bot checking thread and post.",pass_context= True)
@commands.has_any_role("Mod","Owner")
async def Timer(msg):
    """
    Change time for bot to regular update.
    Note: Use a Second.
    Also it will take it effect after last timer up.
    For example, timer was 10 min
    now you enter !time 300
    which is 5 min, but you have to wait 10 min or w/e remain min since last post. Once it done, it will replace with 5 min.
    """
    second = (msg.message.content[len('!time'):].strip())
    if second == "":
        await bot.say("You didn't put how many second in!")
    else:
        Main_Config.update({"Second":int(second)})
        await InputFiles(Main_Config, "Config.json")
        if int(second) <=60:
            await bot.say("It is now updated. You have enter {} second".format(second))
        else:
            min = int(second)/60
            await bot.say("It is now updated. You have enter {} second, which is {} min".format(second, format(min,'.2f')))

@bot.command(name="summary",brief="Showing a summary of user",pass_context= True)
async def Summary_stat(msg): #Showing a summary stats of User
    '''
    Give a stat of summary of that username
    Topics Created:
    Posts Created:
    Likes Given:
    Likes Received:
    Days Visited:
    Posts Read:
    '''
    name = (msg.message.content[len('!summary'):].strip())
    if name == "":
        await bot.say("You didn't put name in!")
        return
    data = await Readlinkjson("/users/{}/summary".format(name))
    if "errors" in data:
        await bot.say("{} is not found! Please double check case and spelling!".format(name))
        return
    summary=data["user_summary"]
    print_data= "Topics Created:{}\nPost Created:{}\nLikes Given:{}\nLikes Received:{}\nDays Visited:{}\nPosts Read:{}".format(summary["topic_count"],
                                                                                                                               summary["post_count"],
                                                                                                                               summary["likes_given"],
                                                                                                                               summary["likes_received"],
                                                                                                                               summary["days_visited"],
                                                                                                                               summary["posts_read_count"])
    await bot.say("```py\n{}\n```".format(print_data))

@bot.command(name="stats",breif="Show a Site Statistics",pass_context=True)
async def Statictics(): #To show a stats of website of what have been total post, last 7 days, etc etc
    '''
    Show a table of Topics,Posts, New Users, Active Users, Likes for All Time, Last 7 Days and Lasts 30 Days
    '''
    data=await Readlinkjson("/about")
    stat=data["about"]["stats"]
    await bot.say("""
    ```py
|--------------|----------|--------------|--------------|
|              | All Time | Lasts 7 Days | Last 30 Days |
|--------------|----------|--------------|--------------|
| Topics       |    {0:<6}|      {1:<8}|     {2:<9}|
|--------------|----------|--------------|--------------|
| Posts        |    {3:<6}|      {4:<8}|     {5:<9}|
|--------------|----------|--------------|--------------|
| New Users    |    {6:<6}|      {7:<8}|     {8:<9}|
|--------------|----------|--------------|--------------|
| Active Users |    —     |      {9:<8}|     {10:<9}|
|--------------|----------|--------------|--------------|
| Likes        |    {11:<6}|      {12:<8}|     {13:<9}|
|--------------|----------|--------------|--------------|
```

    """.format(stat["topic_count"],stat["topics_7_days"],stat["topics_30_days"],
               stat["post_count"],stat["posts_7_days"],stat["posts_30_days"],
               stat["user_count"],stat["users_7_days"],stat["users_30_days"],
               stat["active_users_7_days"],stat["active_users_30_days"],
               stat["like_count"],stat["likes_7_days"],stat["likes_30_days"]))


loop = asyncio.get_event_loop()
Main_Config=loop.run_until_complete(Readfiles("Config.json"))
website= Main_Config["link"]
bot.run(Main_Config['username'], Main_Config['password'])
>>>>>>> origin/master
