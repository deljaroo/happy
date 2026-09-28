import os
def call(**kwargs):
	"""
	Takes three to four arguments.
	The first is the name of the file you want to make a trimmed version of.
	Second, where in the video the clip should start.
	Third, how long the resulting video should be.
	A forth optional argument would be the name of the new file.  If left off, it will default to "out" as the name.
	
	This tool uses ffmpeg to make a clipped version of a video file.
	"""
	commands = kwargs['args'] # list of things (seperated by unquoted spaces) typed up after the command that called this script
	path = kwargs['path'].replace('/','\\')
	if len(commands)<3:
		print("Happy needs at least three arguments to run clip.")
		return
	if len(commands)>4:
		print("Happy only accepts 4 arguments for this command so the others will be ignored")
	print("*happily makes that clip for you*") # initial output has a short version of what it does
	out_file_name = "out"
	if len(commands)>3:
		out_file_name = commands[3]
	error_code = os.system(f"ffmpeg -hide_banner -loglevel error -ss {commands[1]} -i {path +"\\"+ commands[0]} -t {commands[2]} -c:v libx264 -c:a copy {path +"\\"+ out_file_name}.mp4")
	if error_code!=0:
		print("Happy reports an error of " + str(error_code))
		print("Happy isn't sure what that means")