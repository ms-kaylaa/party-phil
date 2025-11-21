import discord

import globals
from globals import PREFIX

import asyncio
import importlib
import os
import random
import traceback

from globals import commands_dict, kevin_dict, all_kevins

# -= -- backend!! -- =- #

# loads all modules in a given path into the target_dict
def load_modules(base_path:str, target_dict:dict):
    base_prefix = len(base_path) + 1  # get the index where stuff we care about shows up (end of "{base_path}/")
    
    for root, _, files in os.walk(base_path):
        relative_root = root[base_prefix:].replace(os.sep, ".")  # convert to module path
        if relative_root.startswith("_") or relative_root.endswith("_"):
            continue  # skip backend stuff
        
        for file in files:
            if (not file.endswith(".py")) or file.startswith("_"):
                continue  # skip backend stuff
            
            name = file[:-3]  # remove extension
            module_path = f"{base_path}.{relative_root + '.' if relative_root else ''}{name}"
            target_dict[name] = importlib.import_module(module_path)
            print(f"loaded: {module_path}")

    print(f"finished loading {base_path}")

# broadcast an event to all kevins
async def broadcast(event:str, *args):
    if all_kevins == None:
        print("tried to kevin with no kevin. fuck my kevinless life")
        return

    for module in all_kevins:
        if hasattr(module, event):
            # theres for sure a better way to do this but i dont know how
            event_func = getattr(module, event)

            if len(args) != 0:
                await event_func(client, *args)
            else:
                await event_func(client)

# handle a bot command
async def handle_commands(self:discord.Client, message:discord.Message):
    global commands_dict
    
    # extract command/args
    no_prefix = message.content[len(PREFIX):]

    args = no_prefix.split(" ") # ends up just being args cause of pop
    command = args.pop(0)

    if command in globals.disabled_commands:
        return await message.channel.send("that command has been disabled")

    print(command, args)

    if command in commands_dict:
        await commands_dict[command].run(message, args, self)

# -= -- client!! -- =- #

# NUMBER 1 DIRECTIVE: KEEP IT SIMPLE, STUPID
class Phil(discord.Client):
    async def on_ready(self):
        global all_kevins

        globals.client = self
        
        load_modules("commands", commands_dict)
        load_modules("kevin", kevin_dict)
        all_kevins = list(kevin_dict.values())

        print("my name phil and i ready")
        await self.change_presence(status=discord.Status.online, activity=discord.CustomActivity("Playing Wii Party"))
        
        await broadcast("on_ready")

    async def on_message(self, message:discord.Message):
        EVIL_NICO_USERID = 1338550487414214717
        is_bot = (message.author.bot and not message.author.id == EVIL_NICO_USERID)
        message_is_command = message.content.startswith(PREFIX)

        if is_bot: return

        if message_is_command and not message.content.startswith("ph!add") and random.randint(0, 20) == 9:
            return await message.channel.send("Fuck you! 👎")

        try:
            await broadcast("on_message", message)

            if message_is_command:
                await handle_commands(self, message)
        except Exception as e:
            await message.reply("I errors... `" + str(e)+"`")
            traceback.print_exception(e)

# -= -- login!! -- =- #
def read_token():
    f = open("token.txt")
    for line in f.readlines():
        if not line.startswith("#"):
            return line
        
    return "oops"

intents = discord.Intents.all() # IM LAZY TODO ACTUAL INTENTS
client = Phil(intents=intents)
globals.client = client

# -= -- loop -- =- #
async def main():
    try:
        await client.start(read_token())
    except KeyboardInterrupt:
        print("ahhhh")
    finally:
        print("quitting")

        await broadcast("on_exit")
        await client.close()

        exit()

if __name__ == "__main__":
    asyncio.run(main())