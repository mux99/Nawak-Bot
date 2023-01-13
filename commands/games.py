#GAMES {UPDATE | NEW | RECOUNT} [<message id>]
#
#	[UPDATE] update the already presend message
#		a valid <id> is required
#	[NEW] send the messages again
#	[RECOUNT] update the user count to include new users
#		(dont remove those who left while auto update whas off)

from commands.games_fcts import *
from fcts import readIMG_bytes, readCSV, get_role_from_emoji
from config import *

import discord
import asyncio
import logging
log = logging.getLogger(__name__)

#===EVENTS=============================================================
"""
	remove the role connected to the reaction
	from the user removing it, link made in games.csv
"""
async def remove_user(payload):
	if payload.message_id in [i[0] for i in messages_id]:
		guild = await bot.fetch_guild(payload.guild_id)
		role = get_role_from_emoji(guild,payload.emoji)
		member = await guild.fetch_member(payload.user_id)
		await member.remove_roles(role)


"""
	add the role connected to the reaction
	from the user adding it, link made in games.csv
"""
async def add_user(payload):
	if payload.message_id in [i[0] for i in messages_id]:
		member = payload.member
		role = get_role_from_emoji(member.guild,payload.emoji)
		await member.add_roles(role)

#adding methods to corresponding events (to be called by bot)
listeners["on_raw_reaction_add"].append(add_user)
listeners["on_raw_reaction_remove"].append(remove_user)


#===MAIN-FUNCTION======================================================
async def new(guild,channel):
	data = readCSV(games_path)
	for message in discord.create_message(guild,data):
		await channel.send(message)

async def update(args,guild,channel):
	print(f"-updating: {args}-")
	data = readCSV(games_path)
	for e in guild.text_channels:
		try:
			print("test")
			tmp = await e.fetch_message(int(args[0]))
			await tmp.edit(content=discord.create_message(guild)[int(args[1])])
		except discord.NotFound:
			print("oups")
			continue

async def recount(guild):
	print("-recounting-")
	for _id in messages_id:
		channel = get_channel(guild,_id[1])
		message = await channel.fetch_message(_id[0])
		for reaction in message.reactions:
			role = get_role_from_emoji(guild,reaction.emoji)
			async for user in reaction.users():
				member = await guild.fetch_member(user.id)
				await member.add_roles(role)
	print("-finished-")

def games_C(args, message):
	if message.channel.permissions_for(message.author).administrator == False:
		return
	else:
		loop = asyncio.get_event_loop()
		#send games again & remove old one
		if args[0].upper() == "NEW":
			loop.create_task(new(message.guild,message.channel))
		#update message w/ new infos & recount reactions
		elif args[0].upper() == "UPDATE" and len(args) == 3:
			loop.create_task(update(args,message.guild,message.channel))
		elif args[0].upper() == "RECOUNT":
			loop.create_task(recount(message.guild))