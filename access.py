#!/usr/bin/env python
import sys


# Loops through the user specified file line by line and adds each line to a list. 
file  = sys.argv[1]
lines = []
with open(file) as f:
	lines = f.readlines()

# adds new user 
def useradd(username, password):
	pass

def login(username, password):
	pass
	
def logout():
	pass

def groupadd(groupname):
	pass

def usergrp(username, groupname):
	pass

def mkfile(filename):
	pass
	
def chmod(filename, owner, group, others):
	pass

def chown(filename, username):
	pass		

def chgrp(filename, groupname):
	pass

def read(filename):
	pass

def write(filename, text):
	pass

def execute(filename):
	pass
	
def ls(filename):
	pass

def end():
	pass
	

# Loops through the list of lines split on whitespace.
count = 0
for line in lines:
	command = line.split()
	print(command)
	
	if(command[0] == "useradd"):
		print("useradd")
		
	if(command[0] == "login"):
		print("login")	
		
	if(command[0] == "logout"):
		print("logout")
		
	if(command[0] == "groupadd"):
		print("groupadd")
		
	if(command[0] == "usergrp"):
		print("usergrp")
		
	if(command[0] == "mkfile"):
		print("mkfile")	
		
	if(command[0] == "chmod"):
		print("chmod")
		
	if(command[0] == "chown"):
		print("chown")	
		
	if(command[0] == "chgrp"):
		print("chgrp")
		
	if(command[0] == "read"):
		print("read")	
		
	if(command[0] == "write"):
		print("write")
		
	if(command[0] == "execute"):
		print("execute")
		
	if(command[0] == "ls"):
		print("ls")
		
	if(command[0] == "end"):
		print("end")	
	
