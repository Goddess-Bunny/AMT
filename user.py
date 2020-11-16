import json

class user(object):
	user_info = {'nickname':'', 'name':'', 'last_name':'', 'portfolios':{}}
	
	def __init__(self, choice):
		if choice == 1:
			self.sign_in()
		else:
			self.new_profile()
			
		self.name = self.user_info['name']
		self.nickname = self.user_info['nickname']
		self.last_name = self.user_info['last_name']
		self.portfolios = self.user_info['portfolios']
		self.am_portf = len(self.user_info['portfolios']) # amount of portfolios
		self.portfolio_names = list(self.user_info['portfolios'].keys())
	
	def new_profile(self):
		#---------------------------------------------------------#
		# Function creates a new profile, simultaneously puts     #
		# profile info into user var and into json file.          #
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
		self.user_info['name'] = input('\nYour first name: ')
		
		# 3. last name
		self.user_info['last_name'] = input('\nYour last name: ')
				
		with open('data\\users.json', mode='w', encoding='utf-8') as f: # save new profile
			user.pop('nickname')
			users[nickname] = user
			json.dump(users, f, indent = 2) #rewriting json file with new key (new user)
			self.user_info['nickname'] = nickname
			
		print('\nProfile has been successfully created!\n') 
	
	def sign_in(self):
		#---------------------------------------------------------#
		# Function signs in user into his profile                 #
		# returns: 1 if user found; 0 if there is no such user    #
		#---------------------------------------------------------#
		
		print('\nSign in\n')
		
		nickname = input('Enter your nickname: ')
		
		with open('data\\users.json', mode='r', encoding='utf-8') as f:
			users = json.load(f)

		for u in users.keys(): # loading user info into program memory
			if u == nickname: # found current user
			
				for key in users[u].keys():
					self.user_info[key] = users[u][key]
					
				self.user_info['nickname'] = nickname
				
				break
		else:
			raise ValueError
			
	def get_portfolio(self, portf_name):
		#---------------------------------------------------------#
		# Returns a dictionary with all the info regarding chosen #
		# portfolio.                                              #
		# params: portf_name - str;                               #
		#---------------------------------------------------------#
		
		return self.user_info['portfolios'][portf_name]
		
	def update_user_info(self):
		#---------------------------------------------------------#
		# Function is called each time there is an update to user #
		# info.                                                   #
		# params: user - dict                                     #
		#---------------------------------------------------------#

		with open('data\\users.json', mode='r', encoding='utf-8') as f:
			users = json.load(f)
			
		nickname = self.user_info.pop('nickname') # so logic stays the same (nickname is a key in "user", but in json it's the id)
		users.pop(nickname) # deleting old info
		users[nickname] = self.user_info # putting new info
		
		with open('data\\users.json', mode='w', encoding='utf-8') as f:
			json.dump(users, f, indent=2)
			
		self.user_info['nickname'] = nickname	
		self.am_portf = len(self.user_info['portfolios']) # amount of portfolios
		self.portfolio_names = list(self.user_info['portfolios'].keys())