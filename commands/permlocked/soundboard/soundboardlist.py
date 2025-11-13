import discord
import globals

# this is permlocked so its ok if its a little bad to look at
async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    user = globals.get_user_from_id(message.author.id)

    if not user.has_permission("PLAY_SOUNDBOARD"): return

    targuser = user
    if len(args) > 0:
        try:
            targuser = globals.get_user_from_name(args[0])
        except ValueError:
            return await message.channel.send(f"i don't know anyone named {args[0]}")
        
    if not targuser.has_permission("PLAY_SOUNDBOARD"):
        return await message.channel.send("that user does not have access to the soundboard feature!")
    
    sbs = targuser.soundboard_files
    if len(sbs) == 0:
        return await message.channel.send("that user has no soundboard files!")
    
    await message.channel.send(f"{targuser.discord_user.display_name}'s Soundboards\n{", ".join([sb.name for sb in sbs])}")