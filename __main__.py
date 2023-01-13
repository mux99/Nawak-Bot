from config import *
from fcts import readCSV

from os import getenv

#======================================================================
@bot.event
async def on_ready():
	for f in listeners["on_ready"]: await f()
	print(f"-----connected-----")

@bot.event
async def on_message(message):
	#bot ignores own messages
	if message.author == bot.user: return

	#bot only respond to members(using *)
	if message.content.startswith('*'):
		tmp = message.content.split(" ")
		while "" in tmp:
			tmp.remove("")
		commandHandler(tmp[0][1:],tmp[1:],message,commands_lib)
		await message.delete()

@bot.event
async def on_raw_reaction_add(payload):
	for f in listeners["on_raw_reaction_add"]: await f(payload)

@bot.event
async def on_raw_reaction_remove(payload):
	for f in listeners["on_raw_reaction_remove"]: await f(payload)

#======================================================================
class Command():
	def __init__(self, function, path, name, perm):
		self.funct = function
		self.name = name
		self.manual = ""
		self.perm = perm

		#temporary values
		self.message = None
		with open(path) as file:
			for line in file.readlines():
				if line[0] == "#": self.manual += line[1:]
				else: break

	def call(self, args, message):
		self.returned = ""
		self.message = message
		exec(self.funct+f"({args},commands_lib[\"{self.name}\"].message)")

	def perm_check(self, member):
		#role perm
		if self.perm[0] == "@":
			for i in member.roles:
				if self.perm == i.name:
					return True
		#user perm
		if self.perm[-5] == "#":
			print(f"{member.name}#{member.discriminator}")
			#if self.perm == f"{member.name}#{member.discriminator}"
		return False

def add_command(name, funct, path, perm, lib):
	lib[name] = Command(funct, path, name, perm)

def commandHandler(command, args, message, lib):
	if lib[command].perm_check(message.author):
		try:
			lib[command].call(args, message)
		except:
			tmp = " ".join(args)
			print(f"error calling command: {command} {tmp}")

#======================================================================
if __name__ == '__main__':
	print("--loading--")
	for command in readCSV(commands_path):
		print(f"-loading: {command[0]}-")
		package = ".".join(command[1].split(".")[:-1])
		funct = command[1].split(".")[-1]
		exec(f"from {package} import {funct} as {funct}")
		add_command(command[0],command[1].split(".")[-1],(relativ+"/".join(command[1].split(".")[:-1]))+".py",command[2],commands_lib)
	load_dotenv()
	bot.run(getenv("DICORD_TOKEN"))