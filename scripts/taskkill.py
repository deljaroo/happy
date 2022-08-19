import os
def call(**kwargs):
	"""
	Needs at least one argument; each argument should be the pid of a task
	This forcefully kills all tasks with the given pid list.  It is fine to only provide one pid in the list.
	"""
	commands = kwargs['args']
	if len(commands) < 1:
		print("Happy needs the PID of the task you need ended")
		return
	suffix = "those tasks" if len(commands) > 1 else "that task"
	print("*happily ends "+suffix+"*")
	for pid in commands:
		error_code = os.system("taskkill /f /pid "+str(pid))