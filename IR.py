__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
import json as js
#from scipy import spatial
from numpy import dot
from numpy.linalg import norm

# 透過N-gram生成詞彙和Bag of Word表達文件向量方式, 進行cosine找出最相似的文件
class IR(object):

	def __init__(self):
		# save sentence in data
		self.answer = []
		# n-gram number of character
		self.n = 2
		# read Dic
		self.question = self.read_json('CTBC.json')
		# be used bag in BOW 
		self.bag = self.doc_to_vector()

	def find_best_result(self, query = ""):
		# read dictionary
		with open('doc_vec.txt', 'r') as file:
			json_data = file.read()
			#str to list
			doc_bag = js.loads(json_data)
		# query to vector
		doc = []
		for k in range(len(self.bag)):
			temp = 0
			for i in range(len(query) - 1):
				if self.bag[k] == query[i:i + self.n]:
					temp += 1
			doc.append(temp)
		#print(doc)
		# cosine similarity
		max_score = 0
		max = 0
		#print(type(doc_bag))
		#print(type(doc))
		# Avoid Invalid Value
		doc.append(1)
		for i in range(len(doc_bag)):
			# Avoid Invalid Value
			doc_bag[i].append(1)
			try:
				#result = 1 - spatial.distance.cosine(doc_bag[i], doc)
				result = dot(doc_bag[i], doc) / (norm(doc_bag[i]) * norm(doc))
			except Exception as e:
				print(e)
			else:
				pass
			finally:
				pass
			#print(result)
			if result > max_score:
				max_score = result
				max = i
		return self.answer[max]

	def doc_to_vector(self):
		# create a vocabulary bag, bag目前為list可更改為Set就可直接過濾掉重複的
		bag = []
		for i in range(len(self.question)):
			for j in range(len(self.question[i])):
				if len(bag) == 0:
					bag.append(self.question[i][j])
				else:
					temp = 0
					for k in range(len(bag)):
						if self.question[i][j] != bag[k]:
							temp += 1
					if temp == len(bag):
						bag.append(self.question[i][j])
		#print(bag)
		#print("\n")
		# BOW use n-gram model, and sava vector to dictionary, 這邊以數量進行累加，也可使用TF-IDF進行加權之方法，由於中國信託的問題集每個文件term之重複率不高，故使用前者。
		doc_bag = []
		doc = []
		for i in range(len(self.question)):
			doc = []
			for k in range(len(bag)):
				temp = 0
				for j in range(len(self.question[i])):
					if self.question[i][j] == bag[k]:
						temp += 1
				doc.append(temp)
			doc_bag.append(doc)
		with open('doc_vec.txt', 'w') as file:
			js.dump(doc_bag, file)
		return bag

	def read_json(self, dictioary = None):
		with open(dictioary, 'r', encoding = 'utf-8') as data_file:    
			data = js.loads(data_file.read())
		return self.n_gram(data)

	def n_gram(self, data = None):
		question = []

		for i in range(len(data)):
			temp = []
			string = data[i]['question']
			string1 = data[i]['answer']
			self.answer.append(string1)
			for j in range(len(string) - 1):
				temp.append(string[j: j + self.n])
			question.append(temp)
		#print(question)
		#print("\n")
		return question