import sys
import operator
import os

class utils():

	def getInputFile(self, fileName):

		fullSet = {}
		file = open(fileName)
		lines = file.read().split("\r\n")
		file.close()

		return lines


class TrainingModel():

	def __init__ (self):
		self.trainingSet = {}

	def getTrainingSet(self, fileName):

		print "... Obtaining training set ..."

		tags = {}
		fullSet = {}

		for line in utils().getInputFile(fileName):
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

			#comptar vegades que apareix tag
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
		return (mostFreqTag, self.trainingSet)

class Prediction():

	def __init__ (self):
		self.testSet = []
		self.model = {}
		self.mostFreqTag = 0

	def getTestModel(self, model):
		self.mostFreqTag = model[0]
		self.model = model[1]
		
	def getTestSet(self, fileName):

		print "... Getting test set ..."

		for word in utils().getInputFile(fileName):
			#End of File
			if word == '':
				break
			self.testSet.append(word.decode("latin_1").encode("UTF-8"))

		
	def tagging(self, fileName):

		print "... Tagging test set ..."

		#predictions = []

		file = open(fileName, "w")
		for word in self.testSet:
			if not self.model.has_key(word) :
				#assignar tag mes frequent en el corpus
				file.write( word + "\t" + self.mostFreqTag + "\r\n" )
				#predictions.append((word, self.mostFreqTag))
			else:
				#assignar tag mes frequent de la paraula
				file.write( word + "\t" + self.model[word][0] + "\r\n" )
				#predictions.append((word,self.model[word][0]))

		file.close()


class Accuracy():

	def __init__ (self):
		self.solutions = []
		self.predictions = []

	def computeAccuracy(self, solutions, predsFile):
		print "... Computing accuracy ..."

		self.solutions = utils().getInputFile(solutions)
		self.predictions = utils().getInputFile(predsFile)

		total = 0
		correct = 0.0

		for line in self.predictions :
			if line == self.solutions[total]:
				correct += 1
			total += 1

		return correct / total


class Main():

	#python tagger.py -t t1 -r results.txt 
	model = TrainingModel()
	prediction = Prediction()
	accuracy = Accuracy()

	test, solutions, result = "test_1.txt", "gold_standard_1.txt", "results.txt"
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
		
		i += 1

	genModel = model.getTrainingSet("corpus.txt")		#generate model
	prediction.getTestModel(genModel)					
	prediction.getTestSet(test)
	prediction.tagging(result)							#tag test set
	acc = accuracy.computeAccuracy(solutions, result)	#compute accuracy with gold standard
	print "ACCURACY: ", acc