import discord
import globals

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    user = globals.get_user_from_id(message.author.id)

    if not user.has_permission("MANAGE_COMMANDS"): return

    command = args[0].lower()

    if command in globals.disabled_commands:
        globals.disabled_commands.remove(command)
        await message.channel.send(f"enabled command `{command}`")
    else:
        globals.disabled_commands.append(command)
        await message.channel.send(f"disabled command `{command}`")