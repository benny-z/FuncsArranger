from pprint import pprint
import random

ERROR_MESSAGE = '''
something went terribly wrong
terribbly, terribly wrong
the reason you're hearing this terrible song
is that something went terribly wrong

something apparently broke
completely and totally broke
the python is on fire; there's a whole lot of smoke
i guess something apparently broke

what happened?
we don't exactly know
where was it?
that you were trying to go to
try again i guess
'''

def get_random_subset(iterator, k):
	n = len(iterator)
	if k > n:
		raise(ERROR_MESSAGE)
	indices_to_keep = random.sample(range(0, n), k)
	indices_to_keep.sort()
	return [iterator[index] for index in indices_to_keep]
