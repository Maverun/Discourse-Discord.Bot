import json
import os
import aiohttp

current_dir = os.path.dirname(os.path.realpath(__file__)) # Current path where Read.py is
main_dr = os.path.sep.join(current_dir.split(os.path.sep)[:-2]) #Current Path where Working bot is


#Command and role which is custom command.
with open(current_dir+"/Bot_Config.json") as f:
    Bot_Config = json.load(f)

#Config setting with ID, link,account etc
with open(main_dr+"/Main_Config.json") as f:
    config = json.load(f)

website=config["link"]

async def APIKey():
    key=config["API Key"]
    username=config["API Username"]
    return "?api_key={}&api_username={}".format(key,username)

async def Readlinkjson(name): #read a link and then covert them into json
    api = await APIKey()
    with aiohttp.ClientSession() as session:
        async with session.get(website+name+".json"+api) as resp:
            return(await resp.json())

async def ReadFiles(folder,files):  # Read and get info from the files inside a folder
    with open(os.path.join(folder,files), 'r') as f:
        data = json.load(f)
    print(files, " Read")
    return (data)

async def InputFiles(data,folder,files):  # Input data info into files Inside a folder
    with open(os.path.join(folder,files), 'w') as f:
        json.dump(data, f, indent=2)
    print(files, " Updated")
