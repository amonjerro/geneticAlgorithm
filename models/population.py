import random

class Population:
	def __init__(self,dbObject,startDate,endDate,knpLimit,popLimit):
		self.population = []
		self.db = dbObject
		self.winningCandidate = 0
		self.winningFitness = -99999
		self.startDate = startDate
		self.startData = []
		self.endData = []
		self.endDate = endDate
		self.limit = knpLimit
		self.popLimit = popLimit
		self.stocks = ['Apple','AMD','American Express',
				'Bank of America',"Barclay's",'Banco Santander',
				'Bitcoin','Citibank','Comcast','Disney',
				'Ethereum','Facebook','Fox','Google','HSBC',
				'Intel','Morgan Stanley','Microsoft','Netflix',
				'PayPal','Visa','XRP']
		self.setData()
	def setData(self):
		self.startData = self.db.get('tickerdata',
				['apple_cv','amd_cv','axp_cv',
				'bac_cv','barcl_cv','bsac_cv',
				'btcusd_cv','c_cv','cmcsa_cv',
				'dis_cv','ethusd_cv','fb_cv','fox_cv',
				'goog_cv','hsbc_cv','intl_cv',
				'ms_cv','msft_cv','nflx_cv',
				'pypl_cv','v_cv','xrpusd_cv'],
				['tickerdate','=',self.startDate])
		self.endData = self.db.get('tickerdata',
				['apple_cv','amd_cv','axp_cv',
				'bac_cv','barcl_cv','bsac_cv',
				'btcusd_cv','c_cv','cmcsa_cv',
				'dis_cv','ethusd_cv','fb_cv','fox_cv',
				'goog_cv','hsbc_cv','intl_cv',
				'ms_cv','msft_cv','nflx_cv',
				'pypl_cv','v_cv','xrpusd_cv'],
				['tickerdate','=',self.endDate])
		self.startData = self.startData[0]
		self.endData = self.endData[0]
		self.chromoData = []
		for i in range(len(self.startData)):
			self.chromoData.append({
					'name':self.stocks[i],
					'weight':self.startData[i],
					'profit':self.endData[i] - self.startData[i]
					})
	def populate(self):
		while len(self.population) < self.popLimit:
			self.population.append(list(map(lambda x: random.getrandbits(1),range(len(self.stocks)))))
	def assessFitness(self,chromoArray):
		currentWeight = 0
		fitness = 0
		for i in range(len(chromoArray)):
			if chromoArray[i] and currentWeight + self.chromoData[i]['weight'] < self.limit:
				currentWeight += self.chromoData[i]['weight']
				fitness += self.chromoData[i]['profit']
		if fitness > self.winningFitness:
			self.winningFitness = fitness
			self.winningCandidate = chromoArray
		return fitness
	def getAlpha(self):
		return {'fitness':self.winningFitness,'makeup':self.winningCandidate}
	def getPopulation(self):
		return self.population
	def setPopulation(self,pop):
		self.population = pop[:]


class MatingPool:
	def __init__(self,size):
		self.size = size
		self.pool = []
		self.spawn = []
		self.brackets = []
	def clear(self):
		del self.brackets[:]
		del self.pool[:]
		del self.spawn[:]
	def getBrackets(self):
		return self.brackets
	def getPool(self):
		return self.pool
	def getSpawn(self):
		return self.spawn
	def populate(self, population):
		localCopy = population[:]
		span = len(population)
		sizeCounter = 0
		random.shuffle(localCopy)
		bracket = []
		for i in range(span):
			if sizeCounter == self.size:
				self.brackets.append(bracket)
				bracket = []
				sizeCounter = 0
			if sizeCounter < self.size:
				bracket.append(localCopy.pop())
				sizeCounter += 1
		return
	def struggle(self,fitnessFunct):
		for i in range(len(self.brackets)):
			for j in range(len(self.brackets[i])//2):
				if fitnessFunct(self.brackets[i][j*2]) >= fitnessFunct(self.brackets[i][j*2+1]):
					self.pool.append(self.brackets[i][j*2])
				else:
					self.pool.append(self.brackets[i][j*2+1])
	def singlePointCrossover(self,changePoint):
		pass
	def twoPointCrossover(self,lowPoint,highPoint):
		for i in range(len(self.pool)//2):
			self.spawn.append(self.pool[i*2][:lowPoint] + self.pool[i*2+1][lowPoint:highPoint] + self.pool[i*2][highPoint:])
			self.spawn.append(self.pool[i*2+1][:lowPoint] + self.pool[i*2][lowPoint:highPoint] + self.pool[i*2+1][highPoint:])


def generationEvaluation(generation,fitnessFunct):
	n = len(generation)
	s = sum(map(fitnessFunct,generation))
	return (n,s)

		
