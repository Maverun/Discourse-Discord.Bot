from discord.ext import commands
import datetime
import asyncio
import requests
import json

description = '''Animeforums bot Command List. '''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.uptime = datetime.datetime.utcnow()
    global Data_channel
    Data_channel = bot.get_channel(Config["Data Channel"])
    await timer()

async def timer():
    await latest()
    await asyncio.sleep(Config["Second"])
    await timer()

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

def Readlinkjson(name): #read a link and then covert them into json
    r= requests.get(website+name+".json")
    return json.loads(r.text)

def Readfiles(files):
    with open(files,'r') as f:
        data = json.load(f)
    print(files, " Read")
    return (data)

def InputFiles(data,files):  # Input data info into files Inside a folder
    with open(files, 'w') as f:
        json.dump(data, f, indent=2)
    print(files, " Updated")

async def latest():
    """
    Check if there is any new thread.
    If there is, then add them into a list
    using format of this way
    <Titles>  Author:<Creator>
    <link>

    Note: it will also ignore pinned one if pinned thread is only one post.
    It check if there is no replies, then it is as "new thread"
    """
    Data= []
    old_data=Readfiles("Latest.json")
    json_data=Readlinkjson("/latest")#calling function that will read link json
    for key in json_data["topic_list"]["topics"]:#for each of "latest" titles
        if key["title"] in old_data and key["id"] == old_data[key["title"]]: #if it already exist, then skip
            continue
        if key["posts_count"] == 1: #checking if post itself is only creator, which will show as "new thread"
            post = requests.get(website+"/t/{}.json".format(key['id']))
            json_post = json.loads(post.text)
            for post_data in json_post["post_stream"]["posts"]:
                if post_data["post_number"]==1: #Out of all post, it will get creator username
                    Data.append("{} \tAuthor:{} \n{}".format(key["title"],post_data["username"],website+"/t/"+key["slug"]+"/"+str(key['id'])))
                    old_data.update({key["title"]:key["id"]}) #It will write to files later on so it can check if it already exist and still no replies, poor original poster...
                    print(post_data["username"])
                    print(key["title"])
                    print(key['id'])
                    print("#############################################################")
                    break
    InputFiles(old_data,"Latest.json") #Reason for Json/Dict, beacuse in case Titles are same name but creator may be different
    print("".join(Data))
    print (len("".join(Data)))
    if len("".join(Data)) == 0:
        print ("return")
        return
    elif len("".join(Data)) >=5:
        print("send")
        await bot.send_message(Data_channel,"".join(Data))

@bot.command()
async def uptime():
    """Tells you how long the bot has been up for."""
    await bot.say('I been up for {}'.format(get_bot_uptime()))

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
        Config.update({"Second":int(second)})
        InputFiles(Config,"Config.json")
        if int(second) <=60:
            await bot.say("It is now updated. You have enter {} second".format(second))
        else:
            min = int(second)/60
            await bot.say("It is now updated. You have enter {} second, which is {} min".format(second, format(min,'.2f')))


Config =Readfiles("Config.json")
website= Config["link"]
bot.run(Config['username'], Config['password'])