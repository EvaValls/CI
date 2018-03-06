import sys
import operator
import os

class TrainingModel():

	def __init__ (self):
		self.trainingSet = {}

	def getTrainingSet(self, fileName):
		#1. llegir corpus [paraula, tipus]
		#2. comptar quin tipus aparaiex mes cops
		print "... Obtaining training set ..."

		tags = {}
		fullSet = {}
		file = open(fileName)
		lines = file.read().split("\r\n")
		file.close()
		for line in lines:
			#End of File
			if line == '':
				break

			line = line.decode("latin_1").encode("UTF-8")
			word, tag = line.split()

			#afegim paraula amb valor 1 si el diccionari no la conte
			if not self.trainingSet.has_key(word):
				self.trainingSet[word] = (tag, 1)

			#comprovem si existeix la combinacio paraula-tag i actualitzem valors
			if fullSet.has_key((word,tag)) :
				value = fullSet[(word, tag)] + 1
				fullSet[(word, tag)] = value
				if value > self.trainingSet[word][1]:
					self.trainingSet[word] = (tag, value)
			else:
				fullSet[(word, tag)] = 1

			if tags.has_key(tag) :
				tags[tag] = tags[tag] + 1
			else:
				tags[tag] = 1
		
		return self.generateModel(tags)
		

	def generateModel(self, tags):

		print "... Generating Model ..."

		mostFreqTag = max(tags.iteritems(), key=operator.itemgetter(1))[0]
		file = open("lexic.txt", "w")
		file.write(mostFreqTag)

		dic = self.trainingSet.items()
		for word, tagValue in dic:
			tag, value = tagValue
			file.write( "\n" + word + "\t" + tag + "\t" + str(value) )

		file.close()
		return (self.trainingSet, mostFreqTag)

class Prediction():

	def __init__ (self):
		self.testSet = []
		self.model = {}
		self.mostFreqTag = 0

	def getTestModel(self, fileName, model):
		#1. llegir lexic.txt 
		#2. guardar en model [paraula, tipus, num]
		if model == 0:
			print "... Getting trained model ..."
			#file = open(fileName)
			#...

		self.model = model[0]
		self.mostFreqTag = model[1]
		
	def getTestSet(self, fileName):
		#1. llegir txt
		#2. guardar llista paraules
		print "... Getting test set ..."

		file = open(fileName)
		lines = file.read().split("\r\n")
		file.close()
		for word in lines:
			#End of File
			if word == '':
				break
			self.testSet.append(word.decode("latin_1").encode("UTF-8"))

		
	def tagging(self, fileName, op):
		#1. per cada paraula en testSet
		#1.1 si apareix a model
		#1.1.1 assignar tag
		#1.2 si no
		#1.2.a distancia
		#1.2.b mes frequent
		#2. escriure fitxer results.txt [paraula tipus]
		print "... Tagging test set ..."
		predictions = []
		file = open(fileName, "w")
		for word in self.testSet:
			if not self.model.has_key(word) :
				if op == 0 :
					#Opcio 0 --> assignar tag mes frequent
					file.write( word + "\t" + self.mostFreqTag + "\r\n" )
					predictions.append((word, self.mostFreqTag))
				#elif op == 1:
					#Opcio 1 --> assignar tag de paraula a menys distancia
			else:
				file.write( word + "\t" + self.model[word][0] + "\r\n" )
				predictions.append((word,self.model[word][0]))

		file.close()
		return predictions

class Accuracy():

	def __init__ (self):
		self.solutions = []
		self.predictions = []

	def computeAccuracy(self, solutions, predsFile, predictions):
		#comparar solutions i predictions
		#prediccions correctes / num total
		#retornar accuracy
		print "... Computing accuracy ..."
		print "\t... Getting gold standard test ..."
		self.getInputFile(solutions, "gs")
		print "\t... Getting predictions ..."
		self.getInputFile(predsFile, "p")

		total = 0
		correct = 0.0

		for line in self.predictions :
			if line == self.solutions[total]:
				correct += 1
			total += 1

		return correct / total

		# if predictions == 0:
		# 	print "\t... Getting predictions ..."
		# 	getInputFile(predsFile, "p")
		# else:
		# 	self.predictions = predictions

		# for word, tag in ...

	def getInputFile(self, fileName, fileType):
		#1. llegir fitxer amb solucions i guardar [paraula, tipus]
		wordsList = []
		file = open(fileName)
		wordsList = file.read().split("\r\n")
		file.close()

		if fileType == "gs" :
			#gold standard
			self.solutions = wordsList
		elif fileType == "p":
			#predictions
			self.predictions = wordsList
		else:
			print "ERROR"


class Main():
	#python tagger.py -t t1 -r results.txt -q 0
	model = TrainingModel()
	prediction = Prediction()
	accuracy = Accuracy()
	# narg = len(sys.argv)
	# corpus, test, result, solutions = "", "", "", ""

	# if(narg != 5):
	# 	#default
	# 	corpus = "corpus.txt"
	# 	test = "test_1.txt"
	# 	result = "results.txt"
	# 	solutions = "gold_standard_1.txt"
	# else:
	# 	corpus = sys.argv[1]
	# 	test = sys.argv[2]
	# 	result = sys.argv[3]
	# 	solutions = sys.argv[4]

	test, solutions, result, op = "test_1.txt", "gold_standard_1.txt", "result.txt", 0
	i = 0
	for arg in sys.argv :
		if arg == "-t" :
			if sys.argv[i+1] == "t1":
				test = "test_1.txt"
				solutions = "gold_standard_1.txt"
			if sys.argv[i+1] == "t2":
				test = "test_2.txt"
				solutions = "gold_standard_2.txt"
		if arg == "-r" :
			results = sys.argv[i+1]
		if arg == "-q":
			op = sys.argv[i+1]
		i += 1


	genModel = model.getTrainingSet("corpus.txt")
	prediction.getTestModel("lexic.txt", genModel)
	prediction.getTestSet(test)
	pred = prediction.tagging(result, op)
	acc = accuracy.computeAccuracy(solutions, result, 0)
	print "ACCURACY: ", acc