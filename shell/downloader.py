import subprocess

def sub_call():
	print 'in_sub_call'
	subprocess.call(['echo','hi'])

