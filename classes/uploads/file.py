from classes.userstuff.user import User

import os

class File:
    def __init__(self, source_path:str, owner:User):
        from utils.fileutil import approximate_size
        
        self.path = source_path
        self.owner = owner
        
        lastbitofpath = source_path.split("/")[-1]
        namesplit = lastbitofpath.split(".")
        namesplit.pop()

        self.name = ".".join(namesplit)
        self.name_with_ext = lastbitofpath

        self.time_uploaded = os.path.getctime(source_path)

        

        self.metadata = {}

        self.size = os.path.getsize(source_path)
        self.formatted_size = approximate_size(self.size)

    def get_metadata(self, key):
        return self.metadata.get(key, None)
    
    def set_metadata(self, key, value):
        self.metadata[key] = value

    def inc_metadata(self, key, amt):
        if key not in self.metadata:
            self.metadata[key] = 0
        self.metadata[key] += amt

    def delete(self):
        os.remove(self.path)
        del self.owner.file_metadata[self.name_with_ext]