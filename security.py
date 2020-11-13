from bs4 import BeautifulSoup
from functions import list_of_tickers

available_tickers = []

class security(object):
	name = str()
	exp_ret = 0
	exp_risk = 0

	def __init__(self, name):
		global available_tickers
		
		if len(available_tickers) == 0:
			available_tickers = list_of_tickers()
		
		if name not in available_tickers:
			raise ValueError
		self.name = name
		
	
	
	
			
			