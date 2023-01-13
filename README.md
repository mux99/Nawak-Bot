Nawak Bot

code by Dourov Maxime Dec, 2021

modules: DISCORD | DOTENV | OS(native)

instructions for new commands:
	the function linked to a command name must take two arguments
	-first: a list containing all parameters given
		the arguments are pre treated for types:
			-int are converted
			-float are converted
			-strings are kept as one and the quotes removed
			-everything else is kept as string
	-second: a reference to the Command object


the Command object:

	has six attributes:
		-funct: the name of the fuction attached
		-name: call name of the command
		-path: a direct path to the .py of the command
		-manual: a string of instruction on proper command use

		-message: the reference to the message containing the command call
		-returned: to be modified with the text to return to user (no responces if left empty)


public variables:
	are stored in _commands.py (can be modified by user)
	default ones:
		-command_lib [dict]: holds the Commands objects indexed by call names
		-listeners [dict of Arrays]: every function referenced in the lists
			is called when the corresponding event is trigered
			!! the fuction is always given the same parameters as the event calling it!!