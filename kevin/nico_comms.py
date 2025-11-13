import discord
import globals

import json

EVIL_NICO_USER_ID = 1338550487414214717
COMM_CHANNEL_ID = 1432870220191629528

PAYLOAD_HEADER = "PAYLOAD | "
REQUEST_HEADER = "REQUEST | "

async def on_message(client:discord.Client, message:discord.Message):
    if message.author.id == EVIL_NICO_USER_ID and message.channel.id == COMM_CHANNEL_ID:
        header, data = message.content.split(" | ")
        data = json.loads(data)

        if message.content.startswith(PAYLOAD_HEADER):
            type = data['type']
            commanddata = data['data']

            match type:
                case 'command':
                    await message.channel.send("SUCCESS | i know what this command means!")

                case 'givecoin':
                    userid = commanddata['user']
                    amt = commanddata['amount']

                    user = globals.get_user_from_id(userid)
                    user.inc_property("philcoin", amt)

                    await message.channel.send(f"SUCCESS | added {amt} philcoin to {user.discord_user.display_name}")

                case _:
                    await message.channel.send("FAILURE | i don't know what this means")

        elif message.content.startswith(REQUEST_HEADER):
            type = data['type']
            requestdata = data['data']

            match type:
                case "userproperty":
                    propname = requestdata['propertyname']
                    userid = requestdata['userid']

                    user = globals.get_user_from_id(userid)
                    propvalue = user.get_property(propname)

                    if propvalue == None: propvalue = 0

                    await message.channel.send(f"RESPONSE | {propvalue}")