------
Note: This source code is bit of outdate, won't support most of site as depends on https version.
I now run a bot that you can use mine.
[Click here](http://nurevam.site/)
to get my bot to join on your server.
It will run at every x timer and check if there is new thread for you or not.
Login and select server, then enable Discourse, then put info what is requirement in there.
Then you will have my bot will post when there is new thread.

------



This bot allow to check Discourse if there is any new update thread or not.

Run Bot.py to run it.

It need python 3.5 to work.

Lib require:

Aiohttp v0.19.0

Discord.py async:

**If you run Install Discord.py.bat, it will auto/install Discord.py with aiohttp come in.**
or if you rather have a link of discord.py, which is [this](https://github.com/Rapptz/discord.py). You do not need to install aiohttp at all, unless you get error about import of it which you might need to do manual install it.

Simply replace your email and password of discord account in Config.

Also make sure you get Discord Channel ID for discord reply to.

    Few way to get ID from channel
    -say \#channel
        you will see somthing like <#123456789>, just grab 123456789 part and replace it
    -If viewing on website 
        look at a link, it may be like this https://discordapp.com/channels/5234234234/123456789
        grab last ID after last of /, which is **123456789**
For Owner ID, same way but within "\@user" only

Also, simple replace "Link here" with your own Discourse link in Config.json files.



#Note:
Type !help to see a list of commands

You need to have either "Mod" or "Owner" role in order for !time command work. Otherwise, it will ignore you.
This bot is currently Beta phase.
Planning to add more as I could.

Enjoy.


[MIT License](https://github.com/Maverun/Discourse-Discord.Bot/blob/master/LICENSE)
