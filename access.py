#!/usr/bin/env python
import sys

open("accounts.txt", "w").close()

users = []
current_user = [0]

# Loops through the user specified file line by line and adds each line to a list. 
file  = sys.argv[1]
lines = []
with open(file) as f:
	lines = f.readlines()

# adds new user 
def useradd(username, password):
	if not users and username=="root":
		f = open("accounts.txt" ,"a")
		f.write(username + " " + password+ "\n")
		f.close()
		users.append(username)
	elif current_user[0] == "root":
		f = open("accounts.txt" ,"a")
		f.write(username + " " + password+ "\n")
		f.close()
		users.append(username)
	else:
		print("Only the root user can add new users!")	
	
	

def login(username, password):
	if current_user[0]:
		print("The current user must be logged out before you can login!")
	else:
		with open("accounts.txt") as f:
			accounts = []
			accounts = f.readlines()
			for line in accounts:
				user = line.split()
				if(user[0]==username and user[1]==password):
					current_user[0] = username
					print(current_user[0])
				else:
					print("username or password is wrong!")
def logout():
	current_user[0] = ""

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

	if(command[0] == "useradd"):
		useradd(command[1], command[2])
		
	if(command[0] == "login"):
		login(command[1], command[2])
		
	if(command[0] == "logout"):
		pass
		
	if(command[0] == "groupadd"):
		pass
		
	if(command[0] == "usergrp"):
		pass
		
	if(command[0] == "mkfile"):
		pass
		
	if(command[0] == "chmod"):
		pass
		
	if(command[0] == "chown"):
		pass
		
	if(command[0] == "chgrp"):
		pass
		
	if(command[0] == "read"):
		pass	
		
	if(command[0] == "write"):
		pass
		
	if(command[0] == "execute"):
		pass
		
	if(command[0] == "ls"):
		pass
		
	if(command[0] == "end"):
		pass	
	
