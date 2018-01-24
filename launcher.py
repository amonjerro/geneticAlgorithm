import os
import kernel.db
from models import population

devEnv = False
if 'config' in os.listdir():
	import config.config as cfg
	cfg.setup()

Pop = population.Population(kernel.db.DB(os.environ['DBCONN'],5),'2015-08-06','2016-01-06',2000,100)
MatingPool = population.MatingPool(4)

Pop.populate()

print(population.generationEvaluation(Pop.getPopulation(),Pop.assessFitness))
print(Pop.getAlpha())
for i in range(20):
	print('Generation '+str(i))
	MatingPool.clear()
	MatingPool.populate(Pop.getPopulation())
	MatingPool.struggle(Pop.assessFitness)
	MatingPool.twoPointCrossover(8,16)
	Pop.setPopulation(MatingPool.getSpawn()[:] + MatingPool.getPool()[:])
	Pop.populate()
	print(population.generationEvaluation(Pop.getPopulation(),Pop.assessFitness))
	print(Pop.getAlpha())