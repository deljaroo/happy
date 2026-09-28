import os,random
def call(**kwargs):
	"""
	Takes two arguments:  the first video file name and the second video file name.
	An optional third argument will pick the name of the new file.
	
	This will make a new video file that is the first file directly followed by the second file.
	"""
	commands = kwargs['args'] # list of things (seperated by unquoted spaces) typed up after the command that called this script
	path = kwargs['path'].replace('/','\\')
	if len(commands)<2:
		print("Happy needs exactly two commands to run video merge.")
		return
	if len(commands)>3:
		print("Happy can only merge two files together at once. Run it multiple times if that is what you need.")
		return
	print("*happily makes you a new video that is the combination of those two*") # initial output has a short version of what it does
	out_file_name = "out"
	if len(commands)==3:
		out_file_name = commands[2]
	temp_file_name = ""
	for i in range(8):
		temp_file_name += random.choice("asdfghjklqwertyuiopzxcvbnm1234567890")
	temp_file_name = path + "\\" + temp_file_name + ".txt"
	with open(temp_file_name, "w") as opened:
		to_write = "file '" + path + "\\" + commands[0] +"'\nfile '" + path + "\\" + commands[1] + "'"
		opened.write(to_write.replace("\\","/"))
	error_code = os.system(f"ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i {temp_file_name} -c copy {path +"\\"+ out_file_name}.mp4")
	os.remove(temp_file_name)
	if error_code!=0:
		print("Happy reports an error of " + str(error_code))
		print("Happy isn't sure what that means")