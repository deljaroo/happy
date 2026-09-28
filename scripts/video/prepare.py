import os
def call(**kwargs):
	"""
	Takes one argument to choose what file you want to prepare.
	Takes a second optional argument to choose the name of the new version, otherwise this will name the new file "<original name>prepared"
	
	This tool uses ffmpeg to adjust a video to make sure it will work in a powerpoint
	"""
	commands = kwargs['args'] # list of things (seperated by unquoted spaces) typed up after the command that called this script
	path = kwargs['path'].replace('/','\\')
	if len(commands)<1:
		print("Happy needs to know what file you want to work with.")
		return
	if len(commands)>2:
		print("Happy only accepts 2 arguments for this command so the others will be ignored")
	print("*happily prepares that for you*") # initial output has a short version of what it does
	out_file_name = ".".join(commands[1].split(".")[:-1]) + "prepared" # remove file extension first
	if len(commands)>1:
		out_file_name = commands[1]
	error_code = os.system(f"ffmpeg -i {path +"\\"+ commands[0]} -c:v libx264 -preset slow  -profile:v high -level:v 4.0 -pix_fmt yuv420p -crf 22 -codec:a aac {path +"\\"+ out_file_name}.mp4")
	if error_code!=0:
		print("Happy reports an error of " + str(error_code))
		print("Happy isn't sure what that means")