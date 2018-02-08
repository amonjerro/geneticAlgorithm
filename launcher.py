import os
import kernel.db
from models import population

devEnv = False
if 'config' in os.listdir():
	import config.config as cfg
	cfg.setup()

Pop = population.Population(kernel.db.DB(os.environ['DBCONN'],5),'2015-08-06','2016-01-06',2000,100,20,100)
MatingPool = population.MatingPool(4)

for j in range(100):
	Pop.populate()
	population.generationEvaluation(Pop.getPopulation(),Pop.assessFitness)
	Pop.outputWithAmounts(0)
	for i in range(30):
		MatingPool.clear()
		MatingPool.populate(Pop.getPopulation())
		MatingPool.struggle(Pop.assessFitness)
		MatingPool.twoPointCrossover(8,16,('genes','amounts'))
		MatingPool.mutate(.01,('genes','amounts'),Pop.getPurchaseAmount)
		Pop.setPopulation(MatingPool.getSpawn()[:] + MatingPool.getPool()[:])
		Pop.populate()
	Pop.outputWithAmounts(1)

	Pop.reset()