#IP [private method]
#	return the public ip of the discord bot

import requests

def get_ip_C(args,message):
	response = requests.get('https://api.ipify.org')
	message.channel.send(response.text,delete_after=25)