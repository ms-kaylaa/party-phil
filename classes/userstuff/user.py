import discord

from classes.userstuff.permission import Permission

import json
import os

from typing import Any

KAYLA_USERID = 1135951334651207701

def read_json(path):
	with open(path, "r") as f:
		return json.load(f)

DEFAULT_PROPS = {
	"permissions": [],
	"property_dict": {}
}

DEFAULT_FILE_METADATA = {
	"reactions": {},
	"times_gotten": 0,
	"pinned": False
}

class User:	
	USER_DIR = "userdata/"

	# -- CONSTRUCTOR -- #
	def __init__(self, base_user:discord.User):
		self.discord_user = base_user

		self.id = base_user.id

		self.user_dir = f"{User.USER_DIR}{base_user.id}"
		if not os.path.exists(self.user_dir):
			os.makedirs(self.user_dir)

		prop_path = f"{self.user_dir}/userproperties.json"
		if not os.path.exists(f"{self.user_dir}/userproperties.json"):
			with open(prop_path, 'w') as f:
				json.dump(DEFAULT_PROPS, f, indent=4)

		prop_json = read_json(prop_path)

		self._permissions = [Permission(perm) for perm in prop_json['permissions']]
		self._properties = prop_json['property_dict']

		stats_path = f"{self.user_dir}/userstats.json"
		if not os.path.exists(stats_path):
			with open(stats_path, 'w') as f:
				json.dump({}, f, indent=4)

		self.stats = read_json(stats_path)

		self.file_metadata:dict = None



	# -- FACTORIES -- #
	@staticmethod
	def from_id(id:int):
		from globals import client

		base_user = client.get_user(id)
		if base_user is None:
			raise ValueError(f"no user with id {id} found")

		return User(base_user)
	
	def from_name(username:str):
		from globals import client

		base_user = None
		for user in client.users:
			if user.name == username:
				base_user = user
				break
		
		if base_user is None:
			raise ValueError(f"no user with name {username} found")
		
		return User(base_user)



	# -- PROPERTIES -- #
	@property
	def name(self) -> str: # in case someone switches their user while phil is up
		return self.discord_user.name
	
	@property
	async def full_user(self) -> discord.User:
		from globals import client

		full_user = await client.fetch_user(self.id)

		return full_user
	
	@property
	def files(self):
		from classes.uploads.file import File

		file_path = f"{self.user_dir}/files"
		if not os.path.exists(file_path):
			os.makedirs(file_path)
			return []


		if self.file_metadata == None:
			meta_path = f"{self.user_dir}/file_metadata.json"

			if os.path.exists(meta_path):
				self.file_metadata = read_json(meta_path)
			else:
				print("making metadata json")
				with open(meta_path, 'w') as f:
					json.dump({}, f, indent=4)
				self.file_metadata = {}


		keys = self.file_metadata.keys()
		
		should_save = False
		ret:list[File] = []
		for file in os.listdir(file_path):
			file_obj = File(f"{file_path}/{file}", self)

			if not file in keys:
				should_save = True
				self.file_metadata[file] = DEFAULT_FILE_METADATA

			file_obj.metadata = self.file_metadata[file]

			ret.append(file_obj)

		if should_save:
			self.save()

		return ret
	
	@property
	def soundboard_files(self):
		from classes.uploads.file import File

		soundboard_path = f"{self.user_dir}/soundboard"
		if not os.path.exists(soundboard_path):
			os.makedirs(soundboard_path)
			return []
		
		ret:list[File] = []
		for file in os.listdir(soundboard_path):
			ret.append(File(f"{soundboard_path}/{file}", self))
			
		return ret
	
	
	
	def save(self) -> None:
		prop_path = f"{self.user_dir}/userproperties.json"
		with open(prop_path, 'w') as f:
			json.dump({
				"permissions": [perm.name for perm in self._permissions],
				"property_dict": self._properties
			}, f, indent=4)

		stats_path = f"{self.user_dir}/userstats.json"
		with open(stats_path, 'w') as f:
			json.dump(self.stats, f, indent=4)

		meta_path = f"{self.user_dir}/file_metadata.json"
		with open(meta_path, 'w') as f:
			json.dump(self.file_metadata, f, indent=4)
	
	
	# property funcs
	def set_property(self, property:str, value:Any) -> None:
		self._properties[property] = value

		self.save()

	def inc_property(self, property:str, diff:float):
		if property not in self._properties:
			self._properties[property] = 0
		self._properties[property] += diff

		self.save()

	def get_property(self, property:str) -> Any:
		return self._properties.get(property, None)

	# permission funcs
	def grant_permission(self, permission) -> None:
		if isinstance(permission, str):
			permission = Permission(permission.upper())
		
		self._permissions.append(permission)
		self.save()

	def has_permission(self, permission) -> bool:
		if self.id == KAYLA_USERID: return True

		if isinstance(permission, str):
			permission = Permission(permission.upper())
		return permission in self._permissions
	
	# whatever
	def __str__(self):
		return f"User({self.name}, {self.id})"