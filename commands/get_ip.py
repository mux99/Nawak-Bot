#IP [private method]
#	return the public ip of the discord bot

import requests
import asyncio

def get_ip_C(args,message):
	async def send(msg,channel):
		await channel.send(msg,delete_after=25)
	loop = asyncio.get_event_loop()
	response = requests.get('https://api.ipify.org')
	loop.create_task(send(response.text,message.channel))