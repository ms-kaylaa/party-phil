import discord

from classes.userstuff.user import User
from classes.uploads.file import File

PREFIX = "ph!"

USER_DIR = User.USER_DIR
GEN_DIR = "gens/"

commands_dict = {}
kevin_dict = {} # you gotta be fucking kidding me
all_kevins = []

client:discord.Client = None
bot_loop = None

users:list[User] = None
disabled_commands:list[str] = []

kevin_globals:dict = {} 

def get_user_from_name(username:str):
    for user in users:
        if user.name == username:
            return user
    
    newuser = User.from_name(username)
    return newuser

def get_user_from_id(id:int):
    for user in users:
        if user.id == id:
            return user
    
    newuser = User.from_id(id)
    return newuser

def get_all_files():
    ret:list[File] = []
    for user in users:
        ret += user.files
    return ret