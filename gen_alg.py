import random
from collections import namedtuple
import utils
from pprint import pprint
import math

Func = namedtuple("func", ['id', 'length'])

class GenAlg:
	def __init__(self, calls_matrix, funcs_length):
		self.calls_matrix = calls_matrix
		self.funcs_length = funcs_length
		self.pop_size = 3
		self.generations = 20
		self.mutation_prob = 2 # in percents

	def __get_abs_location(self, gene, index):
		return sum([func.length for func in gene[:index]])

	def __generate_init_population(self, num_of_funcs):
		population = []
		pop_size = min(math.factorial(num_of_funcs), self.pop_size)
		for i in range(pop_size+1):
			gene = range(1,num_of_funcs+1)
			gene = [Func(id = j, length=self.funcs_length[j]) for j in gene]
			random.shuffle(gene)
			population.append(gene)
		return population

	def get_pop_ordered_by_fitness(self, population):
		fitness = map(self.fitness, population)
		sorted_fitness = fitness
		sorted_fitness.sort()
		return [population[fitness.index(i)] for i in sorted_fitness], sorted_fitness

	def run(self):
		num_of_funcs = self.calls_matrix.shape[0]
		population = self.__generate_init_population(num_of_funcs)
		for i in range(self.generations):
			sorted_population, sorted_fitness = self.get_pop_ordered_by_fitness(population)
			
			gene1 = population[-1] # best gene
			gene2 = population[-2] # second best gene

			max_fitness = sorted_fitness[-1]
			second_max_fitness = sorted_fitness[-2]

			offspring = self.crossover(gene1, gene2, max_fitness, second_max_fitness)		
			
			# replacing the gene with the minimal fitness function
			sorted_population[0] = offspring

			# mutating
			for i in range(self.pop_size):
				if self.mutation_prob > int(random.uniform(0,100)):
					sorted_population[i] = self.mutate(sorted_population[i])

			population = sorted_population
		best_gene = population[-1]
		return [func.id for func in best_gene]

	def mutate(self, gene):
		gene_len = len(gene)
		i = 0
		j = 0
		while i == j:
			i = int(random.uniform(0, gene_len))
			j = int(random.uniform(0, gene_len))
		gene[i], gene[j] = gene[j], gene[i]
		return gene

	def crossover(self, gene1, gene2, gene1_fitness, gene2_fitness):
		# Union Crossover Algorithm 2 from:
		# http://ac.els-cdn.com/0305054893E0024N/1-s2.0-0305054893E0024N-main.pdf?_tid=f74df37e-40b7-11e5-84b6-00000aab0f6c&acdnat=1439359637_3082e8872ec28fad76a5e6efda773012
		# (page 7)
		num_of_funcs = len(gene1)
		accu_fitness = gene1_fitness + gene2_fitness
		num_of_funcs_from_gene1 = int((num_of_funcs * gene1_fitness) // accu_fitness)

		s1 = set(utils.get_random_subset(gene1, num_of_funcs_from_gene1))
		s2 = set([gene2[i] for i in range(num_of_funcs) if gene2[i] not in s1])
		offspring = []
		while len(offspring) != num_of_funcs:
			if bool(random.getrandbits(1)) and len(s1) != 0:
				offspring.append(s1.pop())
			elif len(s2) != 0:
				offspring.append(s2.pop())
			elif len(s1) == len(s2) == 0:
				continue
		return offspring

	def fitness(self, gene):
		gene_size = len(gene)
		fitness = 0
		for i in range(gene_size):
			for j in range(gene_size):
				func1 = gene[i]
				func2 = gene[j]
				num_of_calls = self.calls_matrix[i][j]
				func1_location = self.__get_abs_location(gene, i)
				func2_location = self.__get_abs_location(gene, j)
				dist_between_funcs = func1_location - func2_location
				# the distance between a function and itself is zero so there is no need
				# to check whether we're sorting the same function
				fitness += num_of_calls * dist_between_funcs

		return 1 / float(fitness)