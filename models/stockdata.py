
class StockData:
	def __init__(self,startDate,endDate):
		self.stocks = ['Apple','AMD','American Express',
				'Bank of America',"Barclay's",'Banco Santander',
				'Bitcoin','Citibank','Comcast','Disney',
				'Ethereum','Facebook','Fox','Google','HSBC',
				'Intel','Morgan Stanley','Microsoft','Netflix',
				'PayPal','Visa','XRP']
		self.startDate = startDate
		self.endDate = endDate
		def setData(self):
			self.data = self.db.get('tickerdata',
					['apple_cv','amd_cv','axp_cv',
					'bac_cv','barcl_cv','bsac_cv',
					'btcusd_cv','c_cv','cmcsa_cv',
					'dis_cv','ethusd_cv','fb_cv','fox_cv',
					'goog_cv','hsbc_cv','intl_cv',
					'ms_cv','msft_cv','nflx_cv',
					'pypl_cv','v_cv','xrpusd_cv'],
					['tickerdate','>=',self.startDate,'AND','tickerdate','<=',self.endDate])
			self.startData = self.data[0]