import json
import ctypes
import os

def sign_in(user):
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
    while(True):
        try:
            print('Choose an option: ', end='')
            choice = int(input())
            break
        except ValueError:
            print('Incorrect input')
            
    return choice
    
def update_user_info(user):
	with open('data\\users.json', mode='r', encoding='utf-8') as f:
		users = json.load(f)
		
	nickname = user.pop('nickname') # so logic stays the same (nickname is a key in "user", but in json it's the id)
	users.pop(nickname) # deleting old info
	users[nickname] = user # putting new info
	
	with open('data\\users.json', mode='w', encoding='utf-8') as f:
		users = json.dump(users, f, indent=2)

def connection(login, password):
	path = os.getcwd()
	lib = ctypes.cdll.LoadLibrary(path+"\\assets\\connect.dll")
	
	log = "<init log_path={} log_level=\"2\" />".format('\"'+path+"\\logs\\"+'\"')

	status_init = lib.InitializeEx(log.encode())

	#<rqdelay> - delay between addressing to the server
	connect = """
<command id=\"connect\">
	<login>TCNN9975</login>
	<password>v6RUG6</password>
	<host>tr1-demo5.finam.ru</host>
	<port>3939</port>
	<language>en</language>
	<rqdelay>20</rqdelay>
	<milliseconds>false</milliseconds>
	<utc_time>true</utc_time>
</command>
	"""
	lib.SendCommand.restype = ctypes.c_char_p

	status_connect = lib.SendCommand(connect.encode())
	
def exit():
	path = os.getcwd()
	lib = ctypes.cdll.LoadLibrary(path+"\\assets\\connect.dll")
	
	lib.SendCommand(b"<command id=\"disconnect\"/>")
	
	lib.UnInitialize()