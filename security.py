from bs4 import BeautifulSoup
from functions import send_command, free_memory, read_callback, error_handling

availiable_tickers = []

def list_of_tickers(arr):
	#---------------------------------------------------------#
	# Function pulls a list of all tickers on market.         #
	# params: arr - list                                      #
	#---------------------------------------------------------#

	err = send_command(r'<command id="get_securities" />')
	
	if err:
		raise SystemExit
		
	xml = read_callback()
	
	

class security(object):
	name = str()

	def __init__(self, name):
		self.name = name
		
		
	
	
			
			