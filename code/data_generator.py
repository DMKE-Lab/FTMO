import json
import random

def train_generate(datapath, batch_size, few, symbol2id, ent2id, e1rel_e2):
	train_tasks = json.load(open(datapath + '/train_tasks.json'))
	rel2candidates = json.load(open(datapath + '/rel2candidates_all.json'))
	task_pool = list(train_tasks.keys())
	#print (task_pool[0])

	num_tasks = len(task_pool)

	# for query_ in train_tasks.keys():
	# 	print len(train_tasks[query_])
	# 	if len(train_tasks[query_]) < 4:
	# 		print len(train_tasks[query_])

	print("train data generation")

	rel_idx = 0

	while True:
		if rel_idx % num_tasks == 0:
			random.shuffle(task_pool)
		query = task_pool[rel_idx % num_tasks]
		#print (query)
		rel_idx += 1

		#query_rand = random.randint(0, (num_tasks - 1))
		#query = task_pool[query_rand]

		candidates = rel2candidates[query]
		#print rel_idx

		if len(candidates) <= 20:
			continue

		train_and_test = train_tasks[query]
		random.shuffle(train_and_test)

		support_triples = train_and_test[:few]
		# print(symbol2id)
		# print(support_triples)
		# for triple in support_triples:
		# 	print(triple[0])
		# print(train_and_test)
		support_pairs = [[symbol2id.get(str(triple[0])), symbol2id.get(str(triple[2]))] for triple in support_triples]
		# support_pairs = [[symbol2id[str(triple[0])], symbol2id[str(triple[2])]] for triple in support_triples]
		# print(support_pairs)
		support_left = [ent2id.get(str(triple[0])) for triple in support_triples]
		support_right = [ent2id.get(str(triple[2])) for triple in support_triples]
		# print(support_left)
		# print(support_right)
		# print(support_right)
		# support_left = [ent2id[triple[0]] for triple in support_triples]
		# support_right = [ent2id[triple[2]] for triple in support_triples]

		all_test_triples = train_and_test[few:]

		if len(all_test_triples) == 0:
			continue

		if len(all_test_triples) < batch_size:
			query_triples = [random.choice(all_test_triples) for _ in range(batch_size)]
		else:
			query_triples = random.sample(all_test_triples, batch_size)
		# print(query_triples)
		# query_pairs = [[symbol2id[triple[0]], symbol2id[triple[2]]] for triple in query_triples]
		query_pairs1 = [[symbol2id.get(str(triple[0])), symbol2id.get(str(triple[2]))] for triple in query_triples]
		# query_left = [ent2id[triple[0]] for triple in query_triples]
		# query_right = [ent2id[triple[2]] for triple in query_triples]
		query_pairs = []
		for q1 in query_pairs1:
			if q1[0] is not None and q1[1] is not None:
				query_pairs.append(q1)
		# print(query_pairs)
		query_left1 = [ent2id.get(str(triple[0])) for triple in query_triples]
		query_right1 = [ent2id.get(str(triple[2])) for triple in query_triples]
		query_left = list(filter(None, query_left1))
		query_right = list(filter(None, query_right1))
		# print(query_left)
		# print(query_right)
		false_pairs = []
		false_left = []
		false_right = []
		for triple in query_triples:
			e_h = triple[0]
			rel = triple[1]
			e_t = triple[2]
			while True:
				noise = random.choice(candidates)
				# print(e1rel_e2)
				if (noise not in e1rel_e2) and noise != e_t:
					break
			false_pairs.append([random.randint(1000, 10000), symbol2id.get(noise)])#1111111111111111111
			false_left.append(ent2id.get(e_h))
			false_right.append(ent2id.get(noise))
			# print(support_pairs)
		# print(len(support_pairs))
		# print(len(query_pairs))
		# print(len(false_pairs))
		# print(len(support_left))
		yield support_pairs, query_pairs, false_pairs, support_left, support_right, query_left, query_right, false_left, false_right


