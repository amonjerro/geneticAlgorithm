import random

class Population:
	def __init__(self,dbObject,startDate,endDate,knpLimit,popLimit,minBuy=0,maxBuy=0):
		#Parameter values
		self.db = dbObject
		self.startDate = startDate
		self.minBuy = minBuy
		self.maxBuy = maxBuy
		self.endDate = endDate
		self.limit = knpLimit
		self.popLimit = popLimit
		
		#Internal Parameter Initialization
		self.winningCandidate = 0
		self.winningFitness = -99999
		self.startData = []
		self.endData = []
		self.population = []

		#This algorithm optimizes based on stock prices. 
		#You could use this as a starter for anything else
		self.stocks = ['Apple','AMD','American Express',
				'Bank of America',"Barclay's",'Banco Santander',
				'Bitcoin','Citibank','Comcast','Disney',
				'Ethereum','Facebook','Fox','Google','HSBC',
				'Intel','Morgan Stanley','Microsoft','Netflix',
				'PayPal','Visa','XRP']
		
		#Begin initialization
		self.setData()
	def reset(self):
		self.winningCandidate = 0
		self.winningFitness = -99999
		del self.population[:]
	def output(self,state):
		with open('outputs.csv','a') as f:
			line = str(state) + ','+ str(self.winningFitness)+','+','.join(map(str,self.winningCandidate))+'\n'
			f.write(line)
	def outputWithAmounts(self,state):
		with open('complexOutput.csv','a') as f:
			line = str(state) + ',' + str(self.winningFitness)
			for i in range(len(self.winningCandidate['genes'])):
				line += ','+str(self.winningCandidate['genes'][i])+','+str(self.winningCandidate['amounts'][i])
			f.write(line+'\n')
	def setData(self):
		#Replace with the columns of your particular database
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
		if self.minBuy:
			purchases = []
			while len(self.population) < self.popLimit:
				del purchases[:]
				individual = list(map(lambda x: random.getrandbits(1),range(len(self.stocks))))
				for i in range(len(individual)):
					if individual[i]:
						purchases.append(random.randint(self.minBuy,self.maxBuy)/self.chromoData[i]['weight'])
					else:
						purchases.append(0)
				self.population.append({'genes':individual[:],'amounts':purchases[:]})
		else:
			while len(self.population) < self.popLimit:
				self.population.append(list(map(lambda x: random.getrandbits(1),range(len(self.stocks)))))
		
	def assessFitness(self,chromoArray):
		currentWeight = 0
		fitness = 0
		if (self.minBuy):
			for i in range(len(chromoArray['genes'])):
				if (chromoArray['genes'][i]) and currentWeight + (self.chromoData[i]['weight']*chromoArray['amounts'][i]) < self.limit:
					currentWeight += self.chromoData[i]['weight'] * chromoArray['amounts'][i]
					fitness += self.chromoData[i]['profit'] * chromoArray['amounts'][i]
		else:
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
	def getPurchases(self):
		return self.purchaseAmounts
	def setPopulation(self,pop):
		self.population = pop[:]
	def getPurchaseAmount(self,stock):
		return random.randint(self.minBuy,self.maxBuy) / self.chromoData[stock]['weight']

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
	def singlePointCrossover(self,changePoint,subData=None):
		if subData:
			for i in range(len(self.pool)//2):
				self.spawn.append({
					subData[0]:self.pool[i*2][subData[0]][:changePoint] + self[i*2+1][subData[0]][changePoint:],
					subData[1]:self.pool[i*2][subData[1]][:changePoint] + self[i*2+1][subData[1]][changePoint:]})
				self.spawn.append({
					subData[0]:self.pool[i*2+1][subData[0]][:changePoint] + self[i*2][subData[0]][changePoint:],
					subData[1]:self.pool[i*2+1][subData[1]][:changePoint] + self[i*2][subData[1]][changePoint:]
					})
		else:
			for i in range(len(self.pool)//2):
				self.spawn.append(self.pool[i*2][:changePoint] + self[i*2+1][changePoint:])
				self.spawn.append(self.pool[i*2+1][:changePoint] + self[i*2][changePoint:])
	def twoPointCrossover(self,lowPoint,highPoint,subData=None):
		if subData:
			for i in range(len(self.pool)//2):
				self.spawn.append(
					{subData[0]:self.pool[i*2][subData[0]][:lowPoint] + self.pool[i*2+1][subData[0]][lowPoint:highPoint] + self.pool[i*2][subData[0]][highPoint:],
					 subData[1]:self.pool[i*2][subData[1]][:lowPoint] + self.pool[i*2+1][subData[1]][lowPoint:highPoint] + self.pool[i*2][subData[1]][highPoint:]
					})
				self.spawn.append(
					{subData[0]:self.pool[i*2+1][subData[0]][:lowPoint] + self.pool[i*2][subData[0]][lowPoint:highPoint] + self.pool[i*2+1][subData[0]][highPoint:],
					 subData[1]:self.pool[i*2+1][subData[1]][:lowPoint] + self.pool[i*2][subData[1]][lowPoint:highPoint] + self.pool[i*2+1][subData[1]][highPoint:]
					})
		else:
			for i in range(len(self.pool)//2):
				self.spawn.append(self.pool[i*2][:lowPoint] + self.pool[i*2+1][lowPoint:highPoint] + self.pool[i*2][highPoint:])
				self.spawn.append(self.pool[i*2+1][:lowPoint] + self.pool[i*2][lowPoint:highPoint] + self.pool[i*2+1][highPoint:])
	def mutate(self, mutationRate,subData=None,amounter=None):
		if subData:
			for i in range(len(self.pool)):
				if random.random() <= mutationRate:
					print('Mutating!')
					chromosomeToMutate = random.randint(0,len(self.pool[i][subData[0]])-1)
					final_val = abs(self.pool[i][subData[0]][chromosomeToMutate]-1)
					self.pool[i][subData[0]][chromosomeToMutate] = final_val
					self.pool[i][subData[1]][chromosomeToMutate] = amounter(chromosomeToMutate) * final_val
		else:
			for i in range(len(self.pool)):
				if random.random() <= mutationRate:
					print('Mutating!')
					chromosomeToMutate = random.randint(0,len(self.pool[i])-1)
					self.pool[i][chromosomeToMutate] = abs(self.pool[i][chromosomeToMutate]-1)


def generationEvaluation(generation,fitnessFunct):
	n = len(generation)
	s = sum(map(fitnessFunct,generation))
	return s/n
