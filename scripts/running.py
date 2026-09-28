import os

def call(**kwargs):
	"""
	Requires one argument:  the name of the process you want to check for
	
	This tool checks tasklist to show you if a particular item is in there
	"""
	commands = kwargs['args'] # list of things (seperated by unquoted spaces) typed up after the command that called this script
	path = kwargs['path'].replace('/','\\')
	if len(commands)<1:
		print("Happy needs to know what you'd like to check.")
		return
	if len(commands)>1:
		print("Happy only wants one argument so the extras will be ignored")
	print("*happily checks if that is running*") # initial output has a short version of what it does
	to_execute = "tasklist | find /i \"" + commands[0] + "\""
	error_code = os.system(to_execute)