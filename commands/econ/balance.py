import discord
import globals

KAYLA_USERID = 1135951334651207701
async def run(message: discord.Message, args: list[str], client: discord.Client = None):

    user = globals.get_user_from_id(message.author.id)

    balance = user.get_property("philcoin")
    if balance == None: balance = 0

    return await message.channel.send(f"{user.discord_user.display_name.lower()}'s philcoin balance: {balance}\nNOTE: philcoin is deprecated and may be removed at any time. it can no longer be gained or lost")