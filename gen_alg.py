import random
from collections import namedtuple
from math import abs

func = namedtuple("func", "id name location")
gene = namedtuple("gene", )

class GenAlg:
	def __init__(self, calls_matrix):
		self.calls_matrix = calls_matrix
		# self.calls_matrix =	[[1,44,3], /
							 # [7,6 ,1], /
							 # [5,6 ,1]]
		

	def __prepare_gene(self, num_of_funcs):
		pass

	def run(self):
		gene = self.__prepare_gene()

	def mutate(self, gene):
		gene_len = len(gene)
		i = 0
		j = 0
		while i == j:
			i = random.uniform(0, gene_len)
			j = random.uniform(0, gene_len)
		gene[i], gene[j] = gene[j], gene[i]
		return gene

	def crossover(self, gene1, gene2, gene1_fitness, gene2_fitness):
		child_gene = []
		pass

	def fitness(self, gene):
		gene_size = len(gene)
		fitness = 0
		for i in range(gene_size):
			for j in range(gene_size):
				func1 = gene[i]
				func2 = gene[j]
				num_of_calls = self.calls_matrix[i][j]
				dist_between_funcs = func1.location - func2.location
				# the distance between a function and itself is zero so there is no need
				# to check whether we're sorting the same function
				fitness += num_of_calls * dist_between_funcs

		return 1 / float(fitness)