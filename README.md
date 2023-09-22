# Genetic Algorithm

This was an exercise in creating a genetic algorithm in Python.

## Pre-run setup

The exercise was performed using a real-world stock market data as the training dataset. I pulled data for the following stocks:
`'Apple','AMD','American Express',
				'Bank of America',"Barclay's",'Banco Santander',
				'Bitcoin','Citibank','Comcast','Disney',
				'Ethereum','Facebook','Fox','Google','HSBC',
				'Intel','Morgan Stanley','Microsoft','Netflix',
				'PayPal','Visa','XRP'`

To run this system, similar data would need to be pulled. Check the `Population` class to see the names of the columns used. Or don't and create your own data, it's fine.

## How this works

The population is created by extracting data from the day-start and day-end values of a stock to have a measure of the performance of a particular stock.

Individuals in a population start as random arrays of 1s and 0s indicating which stocks were purchased by a particular individual, though there is an option to include the possibility of buying percents or more than unit of a particular stock. The fitness of a particular individual is then calculated by summing up the profits they made that day.

In order for the genetic algorithm to work, in every generation, individuals are separated into competition brackets inside a mating pool. In this implementation, half of the candidates do not make it through this stage - only the top 50% get to spawn new individuals. After spawning new individuals, we test to see if mutations happen and execute those mutations. Finally, we consolidate the mating pool and the spawn as the new population and generate new individuals if we are under the population total.

## Supported algorithms

For reproduction, there are two implemented methods:

- Single point crossover: An index is chosen as the cutoff point and new spawned individuals will have the chromosomes from one parent from before that index and the chromosomes from the other parent after that index.
- Two-point crossover: This selects two indeces and splices the genes based on the three segments these two indeces create

## TO DO

- Spawned children are not subject to mutations, this should be revised
- Currently, spawning plus the old pool fill up the maximum population again.
- Include a way to get setup with sqlite and with locally generated dummy data
