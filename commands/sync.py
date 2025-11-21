import discord
import globals

from globals import commands_dict

from utils import compileallfixed as compileall
import importlib
import os

def walk_path_with_exclusions(base_path:str) -> list[str]:
    ret = []
    for root, _, files in os.walk(base_path):
        if "__pycache__" in root: continue

        for filename in files:
            if filename.startswith("_") or not filename.endswith(".py"): continue
            
            full_path = os.path.join(root, filename)
            ret.append(full_path)

    return ret

from types import ModuleType
def recompile_dir(base_path:str) -> dict[str, ModuleType]:
    ret = {}

    paths = walk_path_with_exclusions(base_path)

    for path in paths:
        pieces = path.split("\\")
        
        file = pieces.pop()
        filename = file[:-3]

        dotted_path = ".".join(pieces)

        # new files
        if filename not in commands_dict:
            ret[filename] = importlib.import_module(dotted_path + "." + filename)
            continue

        # old files
        compiled = compileall.compile_file(path, quiet=True)
        if compiled:
            ret[filename] = importlib.reload(commands_dict[filename])

    # removed files
    current_cmds = list(commands_dict.keys())
    for cmd_name in current_cmds:
        found = False
        for path in paths:
            if path.endswith(f"{cmd_name}.py"):
                found = True
                break
        
        if not found:
            ret[cmd_name] = None

    return ret

async def run(message: discord.Message, args, client: discord.Client):
    msg = await message.channel.send("syncing commands...")
    
    updated_cmds = recompile_dir("commands")

    current_cmds = commands_dict.copy()
    current_cmd_names = list(current_cmds.keys())

    added = []
    updated = []
    removed = []
    
    for cmd_name in updated_cmds.keys():
        if not cmd_name in current_cmd_names:
            added.append(cmd_name)
        elif cmd_name in current_cmd_names and not updated_cmds[cmd_name] == None:
            updated.append(cmd_name)
        elif cmd_name in current_cmd_names and updated_cmds[cmd_name] == None:
            removed.append(cmd_name)

    for name in added + updated:
        commands_dict[name] = updated_cmds[name]
    
    for name in removed:
        del commands_dict[name]

    added_list = (f"added ({len(added)}):\n"
                  f"* {"\n* ".join(added)}\n\n")
    if len(added) == 0:
        added_list = "there were no additions\n\n"

    updated_list = (f"updated ({len(updated)}):\n"
                    f"* {"\n* ".join(updated)}\n\n")
    if len(updated) == 0:
        updated_list = "there were no updates\n\n"

    removed_list = (f"removed ({len(removed)}):\n"
                    f"* {"\n* ".join(removed)}\n\n")
    if len(removed) == 0:
        removed_list = "there were no removals"
        
    send = "finished syncing commands!\n" + added_list + updated_list + removed_list

    await msg.edit(content=send)