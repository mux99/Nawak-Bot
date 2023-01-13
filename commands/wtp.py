#WTP <@player1> <@player2> ...
#
#	give a list of roles in common between listed members
#		the listed members must be correctly @'tted

from config import *
from fcts import readCSV, get_emoji

import asyncio

async def internal(ids,guild,out_channel):
	tmp = {}
	names = {line[1]:(line[0],line[3]) for line in readCSV(games_path)}
	users = []
	for i in ids:
		member = guild.get_member(int(i))
		for role in member.roles:
			if not role.name in roles_blacklist:
				if role.name in tmp.keys():
					tmp[role.name].append(member.name)
				else:
					tmp[role.name] = [member.name]
	out = ", ".join(users)+"Here you go ^^ :\n"
	nothing = True
	reactions = []
	for role, users in tmp.items():
		if len(users) == len(ids):
			nothing = False
			emoji = get_emoji(guild,names[role][1])
			out += f"\t{emoji} {names[role][0]}\n"
			reactions.append(emoji)
	if nothing:
		await out_channel.send("nothing in common..",delete_after=25)
	else:
		await out_channel.send(out[:-1],delete_after=300)

def wtp_C(args,message):
	tmp = args
	for i in range(len(tmp)):
		tmp[i] = tmp[i][2:-1]
	loop = asyncio.get_event_loop()
	loop.create_task(internal(tmp,message.guild,message.channel))