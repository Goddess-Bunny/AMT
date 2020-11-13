import json
import ctypes
import os
import time
from bs4 import BeautifulSoup

path = os.getcwd()
lib = ctypes.WinDLL(path+"\\assets\\connect.dll")
lib.SendCommand.restype = ctypes.POINTER(ctypes.c_char)
lib.InitializeEx.restype = ctypes.POINTER(ctypes.c_char)

dll_callback = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_char))

def historical_info(name):
	#---------------------------------------------------------#
	# Function pulls historical info for specified security   #
	# params: name - str                                      #
	#---------------------------------------------------------#
	pass
	
def list_of_tickers():
	#---------------------------------------------------------#
	# Function pulls a list of all tickers on exchange.       #
	# params: arr - list                                      #
	#---------------------------------------------------------#

	err = send_command(r'<command id="get_securities" />')
	
	if err:
		raise SystemExit
		
	xml = read_callback()
	seccodes = xml.securities.find_all('seccode')
	
	return [name.string for name in seccodes]
	
@dll_callback
def callback(msg):
	# --------- reading from callback ---------- #
	i = 0
	tmp = str()
	
	while True:
		try:
			tmp = tmp + msg[i].decode()
		except UnicodeDecodeError: # found the end of msg
			break
		i+=1
	
	while tmp[i-1] != '>': # strip this string of some strange symbols (no idea where they come from)
		i-=1
	
	tmp = tmp[:i]
	
	# -------------- freeing memory ------------ #
	free_memory(msg)
	
	# -------- parsing callback message -------- #
	with open('tmp\\callback.xml', mode='w', encoding='utf-8') as f:
		f.write(tmp)
	
	return 0

def read_callback():
	#parse callback here
	time_0 = time.time()
	
	while time.time() - 5 < time_0: # wait to listen to callback
		pass
	
	with open("tmp\\callback.xml", mode='r', encoding="utf-8") as f:
		xml = BeautifulSoup(f, 'xml')
		
	return xml

def send_command(command):
	#---------------------------------------------------------#
	# Function sends a command to the server                  #
	# params: command - str (xml)                             #
	# returns: 0 if everything OK; 1 if there is a mistake    #
	#---------------------------------------------------------#
	
	err_ptr = lib.SendCommand(command.encode())
	err = error_handling(err_ptr)
	
	free_memory(err_ptr)
	
	# for a while
	err = 0

	return err

def free_memory(ptr):
	#---------------------------------------------------------#
	# function simply clears memory from messages from server #
	# params: ptr - ctypes.POINTER(ctypes.c_char)             #
	#---------------------------------------------------------#

	err = lib.FreeMemory(ptr)
	
	if not err:
		raise SystemExit

def error_handling(msg):
	# some xml parsing methods
	
	return 0

def sign_in(user):
	#---------------------------------------------------------#
	# Function signs in user into his profile                 #
	# params: user - dict                                     #
	# returns: 1 if user found; 0 if there is no such user    #
	#---------------------------------------------------------#
	
    print('\nSign in\n')
    
    nickname = input('Enter your nickname: ')
    
    with open('data\\users.json', mode='r', encoding='utf-8') as f:
        users = json.load(f)
        
    for u in users.keys(): # loading user info into program memory
        if u == nickname: # found current user
        
            for key in users[u].keys():
                user[key] = users[u][key]
                
            user['nickname'] = nickname
            
            break
    else:
        print('\nCan\'t find a user with this nickname!\n')
        return False
    
    return True
    
def new_profile(user):
	#---------------------------------------------------------#
	# Function creates a new profile, simultaneously puts     #
	# profile info into user var and into json file.          #
	# params: user - dict;                                     #
	#---------------------------------------------------------#
    print('\nCreating a new profile\n')

    with open('data\\users.json', mode='r', encoding='utf-8') as f:
        users = json.load(f)
    
    # 1. nickname
    while(True): # check whether this nickname is free to take
        nickname = input('Your nickname: ')
        
        for u in users.keys():
            if u == nickname:
                print('\nThis nickname has been already taken.\n')
                break
        else: # in order for json to be logically structured, 
              # nickname will be added later in this function
            break
    
    # 2. first name
    user['name'] = input('\nYour first name: ')
    
    # 3. last name
    user['last_name'] = input('\nYour last name: ')
    
    # 4. budget
    while(True): # check if not a number was written, or if negative integer was written
        try:
            user['budget'] = int(input('\nYour current budget (integer in rubles, >= 0): '))
        except ValueError:
            print('\nPlease, enter an integer')
            
        
        if user['budget'] < 0:
            print('\nBudget must be >= 0')
        else:
            break
            
    with open('data\\users.json', mode='w', encoding='utf-8') as f: # save new profile
        user.pop('nickname')
        users[nickname] = user
        json.dump(users, f, indent = 2) #rewriting json file with new key (new user)
        user['nickname'] = nickname
        
    print('\nProfile has been successfully created!\n') 
    
def int_input():
	#---------------------------------------------------------#
	# Function helps prevent ValueError when int(input())     #
	# is called                                               #
	# returns: choice - int
	#---------------------------------------------------------#
    while(True):
        try:
            print('Choose an option: ', end='')
            choice = int(input())
            break
        except ValueError:
            print('Incorrect input')
            
    return choice
    
def update_user_info(user):
	#---------------------------------------------------------#
	# Function is called each time there is an update to user #
	# info.                                                   #
	# params: user - dict                                     #
	#---------------------------------------------------------#

	with open('data\\users.json', mode='r', encoding='utf-8') as f:
		users = json.load(f)
		
	nickname = user.pop('nickname') # so logic stays the same (nickname is a key in "user", but in json it's the id)
	users.pop(nickname) # deleting old info
	users[nickname] = user # putting new info
	
	with open('data\\users.json', mode='w', encoding='utf-8') as f:
		users = json.dump(users, f, indent=2)

def connection(login, password, address, port):
	#---------------------------------------------------------#
	# Function establishes connection with transaq, sets a    #
	# callback function and connects to a server.             #
	# params: login, password, address, port - str;           #
	# returns: 0 if everything OK; 1 if there is a mistake    #
	#---------------------------------------------------------#

	# ------------------ Initializing transaq ----------------------- #
	log_path = '\"'+path+"\\logs\\"+'\"' # specifying the location of logs
	log = f"<init log_path={log_path} log_level=\"2\" />"

	status_init = lib.InitializeEx(log.encode()) # initialize the finam transaq

	if bool(status_init):
		print('Can\'t initialize library. Restart the application')
		free_memory(status_init)
		raise SystemExit
		
	free_memory(status_init)	
	
	# ----------- Setting callback function ------------------------- #
	err = lib.SetCallback(callback)
	
	if not err:
		print('Error! Restart the application')
		raise SystemExit
	
	# -------------- logging in ------------------------------------- #
	login = 'TCNN9975'
	password = 'v6RUG6'
	address = 'tr1-demo5.finam.ru'
	port = '3939'
	
	#<rqdelay> - delay between addressing to the server
	connect = f"""
		<command id=\"connect\">
			<login>{login}</login>
			<password>{password}</password>
			<host>{address}</host>
			<port>{port}</port>
			<language>en</language>
			<rqdelay>10</rqdelay>
			<milliseconds>false</milliseconds>
			<utc_time>true</utc_time>
			
		</command>
	"""
	
	err = send_command(connect)	
	
	time_0 = time.time()
	print('Connecting...')
	while time.time() - 3 < time_0: # wait to listen to all callback from connect
		pass
	
	return error_handling(err)
	
def exit():
	#---------------------------------------------------------#
	# Function is called when the program is terminated       #
	#---------------------------------------------------------#
	err = send_command("<command id=\"disconnect\"/>")
	error_handling(err)
	
	err = lib.UnInitialize()
	
	if bool(err) == True:
		print('Failed to uninitialize. Forced to close the app')
		raise SystemExit
	
	with open('tmp\\callback.xml', mode='w', encoding='utf-8') as f: # make callback.xml empty
		pass