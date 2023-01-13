#natives
import asyncio
#installed
from dotenv import load_dotenv
import discord
from discord import Client, Intents

commands_lib = {
}

listeners = {
	"on_raw_reaction_add":[],
	"on_raw_reaction_remove":[],
	"on_ready":[]
}
relativ = "NawakBot/"
games_path = relativ+"data/games.csv"
commands_path = relativ+"data/commands.csv"

#message id | channel id
messages_id = [
	(917529504744898600,220950045011345408),
	(917529505915105332,220950045011345408),
	(917529506842025984,220950045011345408),
	(917529507974479894,220950045011345408),
	(917529525749973022,220950045011345408),
	(917529526676910100,220950045011345408),
	(917529527373160449,220950045011345408)
]

roles_blacklist=[
	"@everyone","Bots","Mj","Modérateurs","Grande Planificatrice",
	"Quasimodos","Server Booster","membres","Nawak Entertainment",
	"Invitation pour la salle du trône","better airhorn",
	"Automate.io","Mee6","Nawak","parent"
]

games_message_intro = ("@everyone :shinto_shrine: Réagissez pour"
	"rejoindre les équipes des diférents jeux auquels vous jouez."
	"\nSi il faut rajoutez des jeux (multi évidement), tagez @Mux."
	"\n\nListe des jeux par Catégorie:")

#only here to be accesible everywhere (launched in __main__.py)
intents = Intents.all()
bot = Client(intents=intents)