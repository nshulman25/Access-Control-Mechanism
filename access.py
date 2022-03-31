#!/usr/bin/env python
import sys

# clears all text files before execution
open("accounts.txt", "w").close()
open("audits.txt", "w").close()
open("groups.txt", "w").close()
open("files.txt", "w").close()

# variables
users = []
current_user = [0]
groups = {}
files = {}

# Loops through the user specified file line by line and adds each line to a list. 
file  = sys.argv[1]
lines = []
with open(file) as f:
	lines = f.readlines()

# helper func to add to audit file	
def audit(output):	
	print(output)
	f = open("audits.txt" ,"a")
	f.write(output + "\n")
	f.close()	

# terminates if useradd root password is not first command
if "useradd root" not in lines[0]:
	audit("The first command must be in the form \"useradd root password\"")
	quit()


# adds new user 
def useradd(username, password):
	if not users and username=="root":
		f = open("accounts.txt" ,"a")
		f.write(username + " " + password+ "\n")
		f.close()
		users.append(username)
		audit("user " + username + " created")
		
	elif current_user[0] == "root":
		if username in users:
			audit("That username is take already")
		else:	
			f = open("accounts.txt" ,"a")
			f.write(username + " " + password+ "\n")
			f.close()
			users.append(username)
			audit("user " + username + " created")
	else:
		audit("Only the root user can add new users!")	

# logs in specified user. 
# username and password must match in the database
def login(username, password):
	if current_user[0]:
		audit("The current user must be logged out before you can login!")
	else:
		with open("accounts.txt") as f:
			accounts = []
			accounts = f.readlines()
			for line in accounts:
				user = line.split()
				if(user[0]==username):
					if(user[1]==password):
						current_user[0] = username
						audit(current_user[0] + " has logged in")						
					else:
						audit("username or password is wrong!")

# logsout the current user					
def logout():
	if "" in current_user:
		audit("There is currently no user signed in")
	else:
		audit(current_user[0] + " has logged out")
		current_user[0] = ""

# creates group of the specific name
# {groupname: [list of members]}
def groupadd(groupname):
	if current_user[0] == "root":
		if groupname in groups:
			audit("That group already exsists")			
		if "nil" in groups:
			audit("nil is an invalid group name")
		else:
			groups[groupname] = []
			audit("group " + groupname + " created")
	else:
		audit("You do not have root access")
	
# add the specific user to the specific group
def usergrp(username, groupname):
	if current_user[0] == "root":
		if username not in users:
			audit(username + " is not a valid user")
		if groupname not in groups:
			audit(groupname + " is not a valid group")	
		else:
			groups[groupname] += [username]
			audit(username + " added to " + groupname)
	else:
		audit("You do not have root access")

# creates a file of the specified name with default permssions
# {filename: [ownername, groupname, owner, group, other]}
def mkfile(filename):
	if current_user[0] != "":
		if filename in files:
			audit("That file already exsists")			
		elif filename == "accounts.txt":
			audit("accounts.txt is a reserved filename")
		elif filename == "audits.txt":
			audit("audits.txt is a reserved filename")
		elif filename == "groups.txt":
			audit("groups.txt is a reserved filename")
		elif filename == "files.txt":
			audit("files.txt is a reserved filename")			
		else:
			files[filename] = [current_user[0], "nil", "rw-", "---", "---"]
			f = open(filename ,"a")
			f.close()
			audit("file " + filename + " created")
	else:
		audit("A user must be signed in to create a file")

# changes the permssions of the specified file
# changes can only be made by the owner or root
# permisons formated as "rwx" or "---"
def chmod(filename, owner, group, others):
	if current_user[0] != "":
		if filename != "audits.txt" and filename != "accounts.txt" and filename != "groups.txt" and filename != "files.txt":
			if filename in files:
				if current_user[0] == "root" or current_user[0] == files[filename][0]: 
					tempgroup = files[filename][1]

					if len(owner) !=3 or len(group) !=3 or len(others) !=3:
						audit("access permission can only be 3 chars")
					elif owner[0] != "r" and owner[0] != "-":
						audit("the first letter of a permission must be \"r\" or \"-\"")
					elif group[0] != "r" and group[0] != "-":
						audit("the first letter of a permission must be \"r\" or \"-\"")
					elif others[0] != "r" and others[0] != "-":
						audit("the first letter of a permission must be \"r\" or \"-\"")
					elif owner[1] != "w" and owner[1] != "-":
						audit("the second letter of a permission must be \"w\" or \"-\"")
					elif group[1] != "w" and group[1] != "-":
						audit("the second letter of a permission must be \"w\" or \"-\"")
					elif others[1] != "w" and others[1] != "-":
						audit("the second letter of a permission must be \"w\" or \"-\"")
					elif owner[2] != "x" and owner[2] != "-":
						audit("the third letter of a permission must be \"x\" or \"-\"")
					elif group[2] != "x" and group[2] != "-":
						audit("the third letter of a permission must be \"x\" or \"-\"")
					elif others[2] != "x" and others[2] != "-":
						audit("the third letter of a permission must be \"x\" or \"-\"")
					else:
						files[filename] = [current_user[0], tempgroup, owner, group, others]
						audit(filename + " permission have been changed")
				else:
					audit("You do not have permission to access this file")
			else:
				audit("That file does not exsist")
		else:
			audit("You can not modify the " + filename + " file")
	else:
		audit("A user must be signed in to modify a file")


# changes the owner of the specified file
# changes can only be made by root
def chown(filename, username):
	if current_user[0] == "root":
		if username in users:
			if filename != "audits.txt" and filename != "accounts.txt" and filename != "groups.txt" and filename != "files.txt":
				if filename in files:

					files[filename][0] = username
					audit(filename + " owner has been changed")

				else:
					audit("That file does not exsist")
			else:
				audit("You can not modify the " + filename + " file")
		else:
			audit(username + " does not exsist")		
	else:
		audit("Only the root user can change file owners")

# changes the group associated with the specified file
# changes can only be made by root or the owner of the file
# the owner must be a member of the group they are adding the file too	
def chgrp(filename, groupname):
	if current_user[0] != "":
		if filename != "audits.txt" and filename != "accounts.txt" and filename != "groups.txt" and filename != "files.txt":
			if filename in files:
				if current_user[0] == "root" or current_user[0] == files[filename][0]: 
					if groupname in groups:
						if current_user[0] == "root" or current_user[0] in groups[groupname]:

							files[filename][1] = groupname
							audit(filename + " group has been changed")
						else:
							audit(current_user[0] + " can only change the group to one they are a member of")		
					else:
						audit(groupname + " is not a group")	
				else:
					audit("You do not have permission to access this file")
			else:
				audit("That file does not exsist")
		else:
			audit("You can not modify the " + filename + " file")
	else:
		audit("A user must be signed in to modify a file")

# reads the specified file and displays it if the user has the proper permissions
def read(filename):
	if current_user[0] != "":
		if filename != "audits.txt" and filename != "accounts.txt" and filename != "groups.txt" and filename != "files.txt":
			if filename in files:
				if current_user[0] == "root":
					audit("Displaying " + filename)
					with open(filename, 'r') as f:
   						audit(f.read())
				elif current_user[0] == files[filename][0] and files[filename][2][0] == "r":
					audit("Displaying " + filename)
					with open(filename, 'r') as f:
   						audit(f.read())
				elif current_user[0] != files[filename][0] and files[filename][3][0] == "r":
					if files[filename][1] == "nil":
						audit("Displaying " + filename)
						with open(filename, 'r') as f:
   							audit(f.read())
					elif current_user[0] in groups[files[filename][1]]:
						audit("Displaying " + filename)
						with open(filename, 'r') as f:
   							audit(f.read())
					else:
						audit("You are not a member of " + files[filename][1])
				elif current_user[0] != files[filename][0] and files[filename][4][0] == "r":
					audit("Displaying " + filename)
					with open(filename, 'r') as f:
   						audit(f.read())
				else:
					audit("Access Denied")		
			else:
				audit("That file does not exsist")
		else:
			audit("You can not read the " + filename + " file")
	else:
		audit("A user must be signed in to read a file")

def write(filename, text):
	if current_user[0] != "":
		if filename != "audits.txt" and filename != "accounts.txt" and filename != "groups.txt" and filename != "files.txt":
			if filename in files:
				if current_user[0] == "root":
					audit("Writing " + text + "to " + filename)
					f = open(filename, "a")
					f.write(text)
					f.close()
				elif current_user[0] == files[filename][0] and files[filename][2][1] == "w":
					audit("Writing " + text + "to " + filename)
					f = open(filename, "a")
					f.write(text )
					f.close()
				elif current_user[0] != files[filename][0] and files[filename][3][1] == "w":
					if files[filename][1] == "nil":
						audit("Writing " + text + "to " + filename)
						f = open(filename, "a")
						f.write(text)
						f.close()
					elif current_user[0] in groups[files[filename][1]]:
						audit("Writing " + text + "to " + filename)
						f = open(filename, "a")
						f.write(text)
						f.close()
					else:
						audit("You are not a member of " + files[filename][1])
				elif current_user[0] != files[filename][0] and files[filename][4][1] == "w":
					audit("Writing " + text + "to " + filename)
					f = open(filename, "a")
					f.write(text)
					f.close()
				else:
					audit("Access Denied")		
			else:
				audit("That file does not exsist")
		else:
			audit("You can not write to the " + filename + " file")
	else:
		audit("A user must be signed in to write to a file")

def execute(filename):
	if current_user[0] != "":
		if filename != "audits.txt" and filename != "accounts.txt" and filename != "groups.txt" and filename != "files.txt":
			if filename in files:
				if current_user[0] == "root":
					audit(filename + " executed successfully")
				elif current_user[0] == files[filename][0] and files[filename][2][2] == "x":
					audit(filename + " executed successfully")
				elif current_user[0] != files[filename][0] and files[filename][3][2] == "x":
					if files[filename][1] == "nil":
						audit(filename + " executed successfully")
					elif current_user[0] in groups[files[filename][1]]:
						audit(filename + " executed successfully")
					else:
						audit("You are not a member of " + files[filename][1])
				elif current_user[0] != files[filename][0] and files[filename][4][2] == "x":
					audit(filename + " executed successfully")
				else:
					audit("Access Denied")		
			else:
				audit("That file does not exsist")
		else:
			audit("You can not write to the " + filename + " file")
	else:
		audit("A user must be signed in to write to a file")

# displays owner, group, and permissions for a file
def ls(filename):
	if current_user[0] != "":
		if filename != "audits.txt" and filename != "accounts.txt" and filename != "groups.txt" and filename != "files.txt":
			if filename in files:
				audit(filename + ": " + " ".join(files[filename]))
			else:
				audit("That file does not exsist")
		else:
			audit("You can not view the " + filename + " file")
	else:
		audit("A user must be signed in to view a file")

def end():
	audit("Ending session")
	with open("groups.txt" ,"a") as f:
		for key,values in groups.items():
			f.write(key + ": ")
			for v in values:
				f.write(v + " ")
			f.write("\n")			
	f.close()
	
	with open("files.txt" ,"a") as f:
		for key,values in files.items():
			f.write(key + ": ")
			for v in values:
				f.write(v + " ")
			f.write("\n")	
	f.close()
	
	
# password check
def passwordcheck(password):
	if len(password) > 30:
		audit("The password must be less then 30 characters")
		return 1
	else:
		pass

# name check
def namecheck(name):
	if len(name) > 30:
		audit("The name must be less then 30 characters")
		return 1
	if "/" in name or ":" in name:
		audit("The password must be less then 30 characters")
		return 1
	else:
		pass		
		
# Loops through the list of lines split on whitespace.
count = 0
for line in lines:
	command = line.split()

	if(command[0] == "useradd"):
		if passwordcheck(command[2]) == 1 or namecheck(command[1]) == 1:
			break
		else:
			useradd(command[1], command[2])
		
	if(command[0] == "login"):
		login(command[1], command[2])
		
	if(command[0] == "logout"):
		logout()
		
	if(command[0] == "groupadd"):
		if namecheck(command[1]) == 1:
			break
		else:
			groupadd(command[1])
		
	if(command[0] == "usergrp"):
		usergrp(command[1], command[2])
		
	if(command[0] == "mkfile"):
		if namecheck(command[1]) == 1:
			break
		else:
			mkfile(command[1])
		
	if(command[0] == "chmod"):
		chmod(command[1], command[2], command[3], command[4])
		
	if(command[0] == "chown"):
		chown(command[1], command[2])
		
	if(command[0] == "chgrp"):
		chgrp(command[1], command[2])
		
	if(command[0] == "read"):
		read(command[1])	
		
	if(command[0] == "write"):
		write_text = line.split(" ",1)
		write(command[1], write_text[1])
		
	if(command[0] == "execute"):
		execute(command[1])	
		
	if(command[0] == "ls"):
		ls(command[1])
		
	if(command[0] == "end"):
		end()	
