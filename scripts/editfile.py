import os
import subprocess
from pathlib import Path

def call(**kwargs):
	"""
	What arguments does it need?
	What does it do?
	"""
	commands = kwargs['args'] # list of things (seperated by unquoted spaces) typed up after the command that called this script
	path = kwargs['path'].replace('/','\\')
	
	if len(commands)<1:
		print("Happy needs to know what you are searching for")
		return
	if len(commands)>2:
		print("Happy only wants two arguments so the extras will be ignored")
	if len(commands)>1:
		path = os.path.join(path, commands[1])
	query = commands[0]
	to_opens = []
	for root, dirs, files in os.walk(path):
		for file in files:
			if Path(query.casefold()).stem == Path(file.casefold()).stem:
				to_opens.append(os.path.join(root, file))
	lto = len(to_opens)
	if lto==0:
		print("Happy cannot find any files that match that.")
	elif lto > 3:
		print("Happy found " + str(lto) + " files, and it won't open more than three at once.")
	else:
		print("*happily opens files with that name*")
		for to_open in to_opens:
			subprocess.Popen([r"C:\Program Files (x86)\Notepad++\notepad++.exe", to_open])