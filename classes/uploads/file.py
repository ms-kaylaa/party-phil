from classes.userstuff.user import User

import os

class File:
    def __init__(self, source_path:str, owner:User):
        self.path = source_path
        self.owner = owner
        
        lastbitofpath = source_path.split("/")[-1]
        namesplit = lastbitofpath.split(".")
        namesplit.pop()

        self.name = ".".join(namesplit)
        self.name_with_ext = lastbitofpath

        self.time_uploaded = os.path.getctime(source_path)

        self.size = os.path.getsize(source_path)

    def delete(self):
        os.remove(self.path)
        print(self.path)