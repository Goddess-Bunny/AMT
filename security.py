from bs4 import BeautifulSoup
from functions import list_of_tickers, historical_info
from numpy import sqrt

tickers_info = [] # (seccode, board)

class security(object):
	def __init__(self, name, period=None, am_candles=None, weight=None):
		global tickers_info
		
		if len(tickers_info) == 0:
			tickers_info = list_of_tickers()
		
		for seccode, board in tickers_info:
			if name == seccode:
				self.board = board
				self.name = name
				break
		else:
			raise ValueError
		
		if period is not None:
			self.weight = weight
			
			self.data = historical_info(self.name, self.board, period, am_candles) #open, close
			self.exp_ret, self.exp_risk = self.calculate_moments()
		
	def calculate_moments(self):
		sample = [(open+close)/2 for open, close in self.data]
		
		exp_ret = 0
		exp_risk = 0
		
		for i in range(len(sample)-1):
			exp_ret += (sample[i+1]-sample[i])/sample[i]
			
		exp_ret /= (len(sample)-1)
		
		for i in range(len(sample)-1):
			exp_risk += ((sample[i+1]-sample[i])/sample[i]-exp_ret)**2
			
		exp_risk /= (len(sample)-2)
		exp_risk = sqrt(exp_risk)
	
		return (exp_ret, exp_risk)
	
	def cov(self, secur):
		sample1 = [(open+close)/2 for open, close in self.data]
		sample2 = [(open+close)/2 for open, close in secur.data]
	
		exp_cov = 0
	
		for i in range(len(self.data)-1):
			exp_cov += ((sample1[i+1]-sample1[i])/sample1[i] - self.exp_ret)*((sample2[i+1]-sample2[i])/sample2[i] - secur.exp_ret)
			
		exp_cov /= (len(sample1)-1)
			
		return exp_cov
		
	def update_weights(self, weight):
		self.weight = weight