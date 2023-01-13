from config import relativ

def readCSV(filename, separator = ","):
	try:
		with open(filename) as file:
			tmp = [[word.strip() for word in line.split(separator)] for line in file.readlines()]
			for i,e in enumerate(tmp):
				#use (#) as comment indicator
				if e[0][0] == "#": tmp.pop(i)
		return tmp
	except:
		print(f"error loading: {filename}, empty list returned")
		return []

def readIMG_bytes(filename):
	try:
		with open(filename,"rb") as img:
			tmp = img.read()
		return img
	except:
		print(f"error loading: {filename}")

def member_has_role(member,role):
	for tmp_role in member.roles:
		if tmp_role.name == role.name:
			return True
	return False

def get_role_from_emoji(guild,emoji):
	data = readCSV(relativ+"data/games.csv")
	#get the name of the corresponding role
	if type(emoji) is str and emoji[0] == "<":
		name = {line[3][1:]:line[1] for line in data}[emoji.split(":")[1]]
	elif type(emoji) is str:
		emojis = {line[4]:line[1] for line in data}
		name = emojis['U+{:04X}'.format(ord(emoji[0]))]
	elif all(ord(char) > 128 for char in emoji.name):
		emojis = {line[4]:line[1] for line in data}
		name = emojis['U+{:04X}'.format(ord(emoji.name[0]))]
	else:
		name = {line[3][1:]:line[1] for line in data}[emoji.name]

	#get the role object
	for role in guild.roles:
		if role.name == name:
			return role

def get_emoji(guild,name):
	if name[0] != "-":
		return f":{name}:"
	name = name[1:]
	for emoji in guild.emojis:
		if emoji.name == name:
			return f"<:{name}:{str(emoji.id)}>"
	return ""