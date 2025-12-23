import discord
import globals
from globals import client

import asyncio
import math

from classes.userstuff.user import User
from classes.uploads.file import File

FILES_PER_PAGE = 11

LEFT_EMOJI = "⬅️"
RIGHT_EMOJI = "➡️"

from utils.fileutil import approximate_size

class Buttons(discord.ui.View):
    def __init__(self, callbackleft, callbackright, owner:discord.User, max_pages:int, timeout=30):
        super().__init__(timeout=timeout)
        self.callbacks = {
            LEFT_EMOJI: callbackleft,
            RIGHT_EMOJI: callbackright
        }

        self.page = 0
        self.max_pages = max_pages
        self.owner = owner

        self.message:discord.Message = None

    async def on_timeout(self):
        if self.message:
            embed = self.message.embeds[0]
            await self.message.edit(content="*TIMED OUT*", embed=embed, view=None)

    def change_page(self,amt):
        self.page += amt

        self.page = min(self.max_pages-1, max(self.page, 0))

    async def handle(self, interaction:discord.Interaction, button:discord.ui.Button):
        if not interaction.user == self.owner:
            return await interaction.response.defer()
        
        await self.callbacks[str(button.emoji)](button,interaction)

    @discord.ui.button(label="", emoji=LEFT_EMOJI, style=discord.ButtonStyle.blurple)
    async def leftbutton(self,button:discord.ui.Button,interaction:discord.Interaction):
        return await self.handle(button,interaction)

    @discord.ui.button(label="", emoji=RIGHT_EMOJI, style=discord.ButtonStyle.blurple)
    async def rightbutton(self,button:discord.ui.Button,interaction:discord.Interaction):
        return await self.handle(button,interaction)
            
def prepare_embed(user:User, page, discord_user:discord.User) -> discord.Embed:
    rawfiles = user.files

    pinned_files = []
    unpinned_files = []
    for file in rawfiles:
        if file.get_metadata("pinned"):
            print(file.name_with_ext)
            pinned_files.append(file)
        else:
            unpinned_files.append(file)

    files:list[File] = pinned_files + unpinned_files

    max_pages = math.ceil(len(files)/FILES_PER_PAGE)

    size = 0
    for file in files:
        size += file.size
    size_str = approximate_size(size)

    total_size = 0
    for file in globals.get_all_files():
        total_size += file.size
    total_size_str = approximate_size(total_size)

    page_files = files[page*FILES_PER_PAGE:min((page+1)*FILES_PER_PAGE, len(files))]

    desc = ""
    for file in page_files:
        desc += f"*{" 📌" if file.get_metadata("pinned") == True else ""} {file.name_with_ext} ({approximate_size(file.size)})\n"

    embed = discord.Embed(color=discord_user.accent_color,description=desc)
    embed.set_author(name=f"{discord_user.display_name}'s Files",
                    icon_url=discord_user.display_avatar.url)
    embed.set_footer(text=f"Page {page+1}/{max_pages} - {size_str}/{total_size_str} ({math.floor(size/total_size*100)}%)")

    return embed

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    user = None
    if len(args) > 0:
        try:
            user = globals.get_user_from_name(args[0])
        except ValueError:
            return await message.channel.send(f"i don't know anyone named {args[0]}")
    else:
        user = globals.get_user_from_id(message.author.id)

    discord_user = await user.full_user
    
    embed = prepare_embed(user, 0,discord_user)

    async def l(button:discord.ui.Button, interaction:discord.Interaction):
        view = button.view
        view.change_page(-1)

        embed=prepare_embed(user, view.page, discord_user)

        await interaction.response.edit_message(embed=embed, view=view)

    async def r(button:discord.ui.Button, interaction:discord.Interaction):
        view = button.view
        view.change_page(1)

        embed=prepare_embed(user, view.page, discord_user)

        await interaction.response.edit_message(embed=embed, view=view)

    view = Buttons(
        callbackleft=l,
        callbackright=r,
        owner=message.author,
        max_pages=math.ceil(len(user.files)/FILES_PER_PAGE)
    )
    sent = await message.channel.send(embed=embed, view=view)
    view.message = sent