import os
import kernel.db
from models import population

devEnv = False
if 'config' in os.listdir():
	import config.config as cfg
	cfg.setup()

Pop = population.Population(kernel.db.DB(os.environ['DBCONN'],5),'2015-08-06','2016-01-06',2000,100)
MatingPool = population.MatingPool(4)

for j in range(100):
	Pop.populate()

	# print(population.generationEvaluation(Pop.getPopulation(),Pop.assessFitness))
	Pop.output(0)
	for i in range(30):
		# print('Generation '+str(i))
		MatingPool.clear()
		MatingPool.populate(Pop.getPopulation())
		MatingPool.struggle(Pop.assessFitness)
		MatingPool.twoPointCrossover(8,16)
		MatingPool.mutate(.01)
		Pop.setPopulation(MatingPool.getSpawn()[:] + MatingPool.getPool()[:])
		Pop.populate()
		# print(population.generationEvaluation(Pop.getPopulation(),Pop.assessFitness))
		print(Pop.getAlpha())
	Pop.output(1)

	Pop.reset()