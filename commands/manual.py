#HELP [<command name>]
#
#	show specs of the given command or the list of all commands names if none given
from config import *
import asyncio

async def internal(out_channel,args):
	if len(args) == 0:
		await out_channel.send("For more information on a specific command, type HELP command-name\n"+(", ".join(commands_lib.keys())).upper())
	else:
		await out_channel.send(commands_lib[args[0]].manual)


def help_C(args, message):
	loop = asyncio.get_event_loop()
	loop.create_task(internal(message.channel,args))