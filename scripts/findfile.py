import os
def call(**kwargs):
	"""
	It needs one or two arguments.  The first:  a search string, the string of what you are looking for.
	The second argument may be used to tell it where to look relative to current location.  Without it, it will effectively search in the current directory, but it does look in all sub-directories
	
	Searches for files that have a particular string in their name in a directory and all of its sub-directories
	"""
	commands = kwargs['args'] # list of things (seperated by unquoted spaces) typed up after the command that called this script
	path = kwargs['path'].replace('/','\\')
	
	if len(commands)<1:
		print("Happy needs to know what you are searching for")
		return
	if len(commands)>2:
		print("Happy only wants two arguments so the extras will be ignored")
	query = "*" + commands[0] + "*"
	if len(commands)>1:
		query = commands[1] + "\\" + query
	to_execute = 'cd ' + path + ' & dir /s /b ' + query
	#input(to_execute)
	print("*happily searches for files like that*")
	error_code = os.system(to_execute)
	if error_code != 0:
		print("The OS gave back an error to Happy.  Double check your syntax and that the directory you used exists.")