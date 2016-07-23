from discord.ext import commands
from .Utils import Read
import glob
import discord

def Setup(): #Rerun those for refresh variables when reload
    global Config
    global Roles
    global Command
    global Bot_Config
    Config= Read.config
    Roles = Read.Bot_Config["Roles"]
    Command= Read.Bot_Config["cogs"]
    Bot_Config=Read.Bot_Config



def is_owner(msg): #Checking if you are owner of bot
    return msg.message.author.id == Config["Owner"]

def list_cogs(): #Check a list and load it
    cogs = glob.glob("Cogs/*.py")
    clean = []
    for c in cogs:
        c = c.replace("/", "\\") # Linux fix
        clean.append("Cogs." + c.split("\\")[1].replace(".py", ""))
    return clean

class Tools():
    """
    A Tools that is only for owner to control bots
    Such as reload/load/unload cogs(plugins)
    """
    def __init__(self, bot):
        self.bot = bot
        Setup()
        if Bot_Config["Main_Config"]["Greet"]["Enable"] == "on":
            self.bot.add_listener(self.Greet_Message,"on_member_join")

    #Load/Unload/Reload cogs
    @commands.command(hidden=False)
    @commands.check(is_owner)
    async def load(self,*, module : str):
        """Loads a module
        Example: load cogs.mod"""
        module = module.strip()
        if not module in list_cogs():
            await self.bot.say("{} doesn't exist.".format(module))
            return
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
            raise
        else:
            await self.bot.say("Enabled.".format(module))

    @commands.command(hidden=False)
    @commands.check(is_owner)
    async def unload(self,*, module : str):
        """Unloads a module
        Example: unload cogs.mod"""
        module = module.strip()
        if not module in list_cogs():
            await self.bot.say("That module doesn't exist.")
            return
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say("Module disabled.")

    @commands.command(name="reload",hidden=False)
    @commands.check(is_owner)
    async def _reload(self,*, module : str):
        """Reloads a module
        Example: reload cogs.mod"""
        module = module.strip()
        if not module in list_cogs():
            await self.bot.say("This module doesn't exist.".format(module))
            return
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say('\U0001f52b')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
            raise
        else:
            await self.bot.say("Module reloaded.")
    #Load/Unload/Reload cogs

    #Change Command/Role
    @commands.group(name="change",brief="Allow to change either/update roles/commands",pass_context=True,invoke_without_command=True)
    @commands.check(is_owner)
    async def Change(self,msg):
        print(msg.message.content)
        await self.bot.say("Try again with role or command")

    @commands.check(is_owner)
    @Change.command(name="role",brief="Allow to edit role for permission command",pass_context=True,invoke_without_command=True)
    async def Role(self,msg):#Allow to edit/add/remove roles
        await self.bot.say("```py\nCurrently Role list is\n{}\n```".format("\n".join(Roles)))
        await self.bot.say("What do you wish to do, Edit, Remove, or Add")
        answer =await self.bot.wait_for_message(timeout=15,author=msg.message.author)
        print(answer.content)
        if answer.content.lower() == "remove":
            await self.bot.say("Which one do you wish to remove?")
            answer = await self.bot.wait_for_message(timeout=15,author=msg.message.author)
            if answer.content in Roles:
                Roles.remove(answer.content)
                await Read.InputFiles(Read.Bot_Config, "Cogs/Utils", "Bot_Config.json")
            elif answer.content not in Roles:
                await self.bot.say("{} does not exist in first place! Double check spelling?".format(answer.content))
            elif answer is None:
                await self.bot.say("You took too long, restart if you want to update role.")
                return
        elif answer.content.lower() == "edit":
            await self.bot.say("Which one do you wish to edit?")
            answer = await self.bot.wait_for_message(timeout=15,author=msg.message.author)
            if answer.content in Roles:
                await self.bot.say("from {}, what do you wish change to?".format(answer.content))
                new_edit = await self.bot.wait_for_message(timeout=15,author=msg.message.author)
                Roles[answer.content]=new_edit.content
                await Read.InputFiles(Read.Bot_Config, "Cogs/Utils", "Bot_Config.json")
                print(Roles)
            elif answer is None:
                await self.bot.say("You took too long, restart if you want to update role.")
                return
        elif answer.content.lower() == "add":
            await self.bot.say("What do you wish to add")
            answer = await self.bot.wait_for_message(timeout=15,author=msg.message.author)
            if answer.content in Roles:
                await self.bot.say("You already add it!")
            elif answer.content not in Roles:
                Roles.append(answer.content)
                await Read.InputFiles(Read.Bot_Config, "Cogs/Utils", "Bot_Config.json")
                await self.bot.say("{} is updated!".format(answer.content))
            elif answer is None:
                await self.bot.say("You took too long, restart if you want to update role.")
                return
        elif answer is None:
            await self.bot.say("You took too long, restart if you want to update role.")
            return

    @commands.check(is_owner)
    @Change.command(name= "command",brief="Allow to edit command",pass_context=True,invoke_without_command=True)
    async def Command_Edit(self,msg):
        Command_list=[]
        await self.bot.say("```{}```\nWhich Category for command you wish to change".format("".join(Command)))
        cog = await self.bot.wait_for_message(timeout=15,author=msg.message.author)
        print(cog.content)
        if cog.content in Command:
            for name in Command[cog.content]:
                Command_list.append("{0:<2} - !{1:<5}".format(name,Command[cog.content][name]))
            await self.bot.say("```{}```\nWhich Command do you wish to change".format("\n".join(Command_list)))
            command= await self.bot.wait_for_message(timeout=15,author=msg.message.author)
            if command.content in Command[cog.content]:
                await self.bot.say("From {}, what do you wish to change to?".format(command.content))
                edit_command=await self.bot.wait_for_message(timeout=15,author=msg.message.author)
                for cogs in Command:
                    for key in Command[cogs]:
                        print (key)
                        if edit_command.content in Command[cogs][key]:
                            await self.bot.say("You cannot! There is already exist one! Which is under of *{}*, which command was  *{}*\nTry again! ".format(cog,key))
                            return
                if edit_command.content == Command[cog.content][command.content]:
                    await self.bot.say("It is a same command!")
                elif edit_command.content != Command[cog.content][command.content]:
                    Bot_Config["cogs"][cog.content].update({command.content:edit_command.content})
                    await Read.InputFiles(Read.Bot_Config, "Cogs/Utils", "Bot_Config.json")
                    self.bot.unload_extension("Cogs."+cog.content)
                    self.bot.load_extension("Cogs."+cog.content)
                    await self.bot.say("Update!")
                elif edit_command is None:
                    await self.bot.say("You took too long, restart if you want to update command.")
                    return
            elif command is None:
                    await self.bot.say("You took too long, restart if you want to update command.")
                    return
        elif cog is None:
            await self.bot.say("You took too long, restart if you want to update command.")
            return
    #Change Command/Role

    #Greet message
    @commands.group(name="greet",brief="Allow to set up Greet message",pass_context=True,invoke_without_command=True)
    @commands.check(is_owner)
    async def Greet(self,msg):
        print(msg.message.content)
        await self.bot.say("Try again with \"subcommad\" Such as edit , enable and PM options" )

    @commands.check(is_owner)
    @Greet.command(name="edit",brief="Allow to edit the welcome message",pass_context=True,invoke_without_command=True)
    async def Greet_Edit(self,msg):
        await self.bot.say("What do you wish to edit it to?\nNote:\n\t\t{} for username, \n\t\t{1} for mention user")
        answer = await self.bot.wait_for_message(timeout=60,author=msg.message.author)
        if answer is None:
            await self.bot.say("You was taking too long, try again \n Tips:Maybe copy text and then paste?")
            return
        print(answer.content)
        print(Bot_Config["Main_Config"]["Greet"]["Message"])
        Bot_Config["Main_Config"]["Greet"].update({"Message":answer.content})
        await Read.InputFiles(Read.Bot_Config, "Cogs/Utils", "Bot_Config.json")
        await self.bot.say("Updated.")

    @commands.check(is_owner)
    @Greet.command(name="enable",brief="Allow to enable greet message or not",pass_context=True,invoke_without_command=True)
    async def Greet_enable(self,msg):
        await self.bot.say("The currently setting is {}\nWhat do you want to change to(on/off).".format(Read.Bot_Config["Main_Config"]["Greet"]["Enable"]))
        answer = await self.bot.wait_for_message(timeout=15,author=msg.message.author)
        if answer is None:
            print ("You didn't enter any! Try again!")
        elif answer.content == "on" or answer.content == "off":
            if Bot_Config["Main_Config"]["Greet"]["Enable"] == answer.content:
                await self.bot.say("It is already set as {}!".format(answer.content))
            else:
                Bot_Config["Main_Config"]["Greet"].update({"Enable":answer.content})
                await Read.InputFiles(Read.Bot_Config,"Cogs/Utils","Bot_Config.json")
                self.bot.unload_extension("Cogs.Tools")
                self.bot.load_extension("Cogs.Tools")
                await self.bot.say("It is now update")

    @commands.check(is_owner)
    @Greet.command(name="pm",brief="Allow to set for bot to PM user only or in public",pass_context=True,invoke_without_command=True)
    async def Greet_PM(self,msg):
        await self.bot.say("The currently setting is {}\nWhat do you want to change to(on/off).".format(Read.Bot_Config["Main_Config"]["Greet"]["Whisper"]))
        answer = await self.bot.wait_for_message(timeout=15,author=msg.message.author)
        if answer is None:
            print ("You didn't enter any! Try again!")
        elif answer.content == "on" or answer.content == "off":
            if Bot_Config["Main_Config"]["Greet"]["Whisper"] == answer.content:
                await self.bot.say("It is already set as {}!".format(answer.content))
            else:
                Bot_Config["Main_Config"]["Greet"].update({"Whisper":answer.content})
                await Read.InputFiles(Read.Bot_Config,"Cogs/Utils","Bot_Config.json")
                self.bot.unload_extension("Cogs.Tools")
                self.bot.load_extension("Cogs.Tools")
                await self.bot.say("It is now update")

    async def Greet_Message(self,member):
        print(member)
        if Bot_Config["Main_Config"]["Greet"]["Whisper"] == "on":
            await self.bot.send_message(member,Bot_Config["Main_Config"]["Greet"]["Message"].format(member,member.mention))
        else:
            await self.bot.send_message(self.bot.get_channel(member.server.id),Bot_Config["Main_Config"]["Greet"]["Message"].format(member,member.mention))

def setup(bot):
    bot.add_cog(Tools(bot))