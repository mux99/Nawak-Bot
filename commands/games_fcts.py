from config import *
from fcts import get_emoji

def create_messages(guild,data):
	messages = [games_message_intro]
	games_table = {"Autres":[]}
	#gather all infos
	for line in data:
		if line[2] == "-":
			games_table["Autres"].append(line)
		else:
			games_table.setdefault(line[2],[]).append(line)
	#create messages
	for category,games in games_table.items():
		tmp = "**__{}:__**\n".format(category)
		for e in games:
			tmp += "-{}- {}\n".format(get_emoji(guild,e),e[0])
		messages.append(tmp)
	return messages


def get_channel(guild,id_):
	for tmp in guild.text_channels:
		if tmp.id == id_:
			return tmp