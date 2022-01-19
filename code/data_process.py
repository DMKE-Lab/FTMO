import numpy as np
from collections import defaultdict
import json
import matplotlib.pyplot as plt

# distribution of relation triples #
def rel_triples_dis(datapath):
	known_rels = defaultdict(list)
	# with open(datapath + '/other_tasks.json') as f:
	other_tasks = json.load(open(datapath + '/other_tasks.json'))
	for task in other_tasks.keys():
		for quad in other_tasks[task]:
			e1 = quad[0]
			rel = quad[1]
			e2 = quad[2]
			known_rels[rel].append([e1, rel, e2])
		# lines = f.readlines()
		# for line in lines:
		# 	line = line.rstrip()
		# 	#e1,rel,e2 = line.split()
		# 	e1 = line.split()[0]
		# 	rel = line.split()[1]
		# 	e2 = line.split()[2]
		# 	known_rels[rel].append([e1,rel,e2])

	train_tasks = json.load(open(datapath + '/train_tasks.json'))
	#
	for key, triples in train_tasks.items():
		known_rels[key] = triples

	# path_graph (background knowledge) + train_tasks =  known relations
	json.dump(known_rels, open(datapath + '/known_rels.json', 'w'))

	#print len(known_rels)

	# compute distribution
	triple_n_dis = [0] * 5000000
	for key, value in known_rels.items():
		triple_n_dis[len(known_rels[key])] += 1

	fig, axes = plt.subplots()
	plt.plot(triple_n_dis[:100],'-', color='black', linewidth=3, markerfacecolor = 'b')
	fig.subplots_adjust(left=0.15)
	fig.subplots_adjust(bottom=0.2)
	plt.xticks(fontsize=25)
	plt.yticks(fontsize=25)
	plt.xlabel('Relation Frequency',size=25)
	plt.ylabel('Number',size=25)
	plt.grid()
	plt.show()

	# for key, triples in known_rels:
	# 	print len(known_rels[key])


#distribution of relation triples #
def build_vocab(datapath):
	rels = set()
	ents = set()
	other_tasks = json.load(open(datapath + '/other_tasks.json'))
	for task in other_tasks.keys():
		for quad in other_tasks[task]:
			rel = quad[1]
			e1 = quad[0]
			e2 = quad[2]
			rels.add(rel)
			rels.add(str(rel) + '_inv')
			ents.add(e1)
			ents.add(e2)
	# with open(datapath + '/other_tasks.json') as f:
	# 	lines = f.readlines()
	# 	for line in lines:
	# 		# line = line.rstrip()
	# 		rel = line.split(',')[1]
	# 		e1 = line.split(',')[0]
	# 		e2 = line.split(',')[2]
	# 		rels.add(rel)
	# 		rels.add(rel + '_inv')
	# 		ents.add(e1)
	# 		ents.add(e2)
	# print(rels)
	# relation/entity id map
	relationid = {}
	for idx, item in enumerate(list(rels)):
		relationid[item] = idx
	# print(relationid)
	entid = {}
	for idx, item in enumerate(list(ents)):
		entid[item] = idx

	#print len(entid)

	json.dump(relationid, open(datapath + '/relation2ids', 'w'))
	json.dump(entid, open(datapath + '/ent2ids', 'w'))


def candidate_triples(datapath):
	ent2ids = json.load(open(datapath+'/ent2ids'))

	all_entities = ent2ids.keys()
	# print(all_entities)
	type2ents = defaultdict(set)
	for ent in all_entities:
		# print(ent)
		try:
			type_ = ent2ids[ent]
			type2ents[type_].add(ent)
			# print(type_)
			# print(type2ents)
		except Exception as e:
			continue
	#
	train_tasks = json.load(open(datapath + '/known_rels.json'))
	dev_tasks = json.load(open(datapath + '/dev_tasks.json'))
	test_tasks = json.load(open(datapath + '/test_tasks.json'))

	all_reason_relations = list(train_tasks.keys()) + list(dev_tasks.keys()) + list(test_tasks.keys())

	all_reason_relation_triples = list(train_tasks.values()) + list(dev_tasks.values()) + list(test_tasks.values())

	# print(all_reason_relations)
	assert len(all_reason_relations) == len(all_reason_relation_triples)

	rel2candidates = {}
	for rel, triples in zip(all_reason_relations, all_reason_relation_triples):
		possible_types = set()
		for example in triples:
			# print(example)
			try:
				type_ = example[2] # type of tail entity
				possible_types.add(type_)
			except Exception as e:
				print (example)

		candidates = []
		for type_ in possible_types:
			candidates += list(type2ents[type_])

		candidates = list(set(candidates))
		if len(candidates) > 1000:
			candidates = candidates[:1000]
		rel2candidates[rel] = candidates

		#rel2candidates[rel] = list(set(candidates))

	json.dump(rel2candidates, open(datapath + '/rel2candidates_all.json', 'w'))


def for_filtering(datapath, save=False):
	e1rel_e2 = defaultdict(list)
	train_tasks = json.load(open(datapath + '/train_tasks.json'))
	dev_tasks = json.load(open(datapath + '/dev_tasks.json'))
	test_tasks = json.load(open(datapath + '/test_tasks.json'))
	few_triples = []
	for _ in (list(train_tasks.values()) + list(dev_tasks.values()) + list(test_tasks.values())):
		few_triples += _
		# print(few_triples)
	for triple in few_triples:
		e1,rel,e2,t = triple
		e1rel_e2[e1+rel].append(e2)
		# print(e1rel_e2)
	# if save:
	json.dump(e1rel_e2, open(datapath + '/e1rel_e2.json', 'w'))
# if __name__ == '__main__':
# 	candidate_triples('icews')


	





