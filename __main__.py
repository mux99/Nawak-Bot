from os import getenv
from dotenv import load_dotenv
import discord

from config import *
from fcts import readCSV

#======================================================================
@bot.event
async def on_ready():
	for f in listeners["on_ready"]: await f()
	log.info("succesfully connected")

@bot.event
async def on_raw_reaction_add(payload):
	for f in listeners["on_raw_reaction_add"]: await f(payload)

@bot.event
async def on_raw_reaction_remove(payload):
	for f in listeners["on_raw_reaction_remove"]: await f(payload)

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

#======================================================================
class Command():
	def __init__(self, function, path, name, perm):
		self.funct = function
		self.name = name
		self.manual = ""
		self.perm = perm
		self.message = None

		#loading help info
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
			if self.perm == f"{member.name}#{member.discriminator}":
				return True
		return False

def commandHandler(command, args, message, lib):
	try:
		tmp = " ".join(args)
		log.info(f"{message.author.name}#{message.author.discriminator} attempt runing: '{command} {tmp}'")
		if lib[command].perm_check(message.author):
			try:
				lib[command].call(args, message)
			except Exception as e:
				tmp = " ".join(args)
				log.error(f"an error ocured during command call '{command} {tmp}'\n{str(e)}")
		else:
			log.warning(f"access denied to {message.author.name}#{message.author.discriminator} using command '{command}'")
	except KeyError:
		#unknown command, do nothing
		pass

#======================================================================
if __name__ == '__main__':
	discord.utils.setup_logging()

	for command in readCSV(commands_path):
		try:
			package = ".".join(command[1].split(".")[:-1])
			funct = command[1].split(".")[-1]
			exec(f"from {package} import {funct} as {funct}")
			commands_lib[command[0]] = Command(command[1].split(".")[-1], (relativ+"/".join(command[1].split(".")[:-1]))+".py", command[0], command[2])
		except Exception as e:
			log.error(f"error loading {funct}\n{str(e)}")
		else:
			log.info(f"succesfully loaded {funct}")
	load_dotenv()
	bot.run(getenv("DICORD_TOKEN"))