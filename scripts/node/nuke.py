import os
def call(**kwargs):
	"""
	No arguments.
	This cleans up the node environment of the current folder
	"""
	commands = kwargs['args'] # list of things typed up after the command that called this script; seperated by unquoted spaces
	path = kwargs['path'].replace('/','\\')
	print("*happily cleans up node*") # initial output has a short version of what it does
	to_execute = "rmdir /s /q " + path + "\\node_modules"
	error_code = os.system(to_execute)
	os.chdir(path)
	to_execute = "yarn cache clean"
	error_code = os.system(to_execute)
	print("Done")