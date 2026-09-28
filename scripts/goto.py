import os, sys
def call(**kwargs):
	"""
	Takes exactly one argument; it will ignore any past the first.
	The argument should be the keyword for a location, and this script will open a new cmd for you at that location.
	If you are unsure of what locations can be gone to or what their keywords are, input an invalid one.
	"""
	commands = kwargs['args'] # list of things (seperated by unquoted spaces) typed up after the command that called this script
	path = kwargs['path'].replace('/','\\')
	if len(commands)<1:
		print("Happy needs to know where you want to go")
		return
	places = {
		'cmj': ['the repo for the Cabells Medicine App', r'Users\Joel\Documents\gitrepos\cabells-journalytics-medicine'],
		'cmm': ['the repo for the Cabells Marketing App', r'Users\Joel\Documents\gitrepos\cabells-marketing-medicine'],
		'cds': ['the repo for the Cabells Design System', r'Users\Joel\Documents\gitrepos\cabells-design-system'],
		'dl': ['the downloads directory', r'Users\Joel\Downloads'],
		'doc': ['documents', r'Users\Joel\Documents'],
		'u': ['your user directory', r'Users\Joel'],
	}
	if commands[0] not in places:
		print("Happy doesn't know that place.  Please use one of the following:")
		for i in places:
			print('\t', i, ": ", places[i][0], sep="")
		return
	picked = places[commands[0]]
	print("*happily takes you to ", picked[0], "*", sep="")
	error_code = os.system("start cmd.exe /K cd C:\\" + picked[1])
	if error_code!=0:
		print("Happy reports an error of " + str(error_code))
		print("Happy isn't sure what that means")
	sys.exit()