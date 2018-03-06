import sys
import operator

class TrainingModel():

	def __init__ (self):
		self.trainingSet = {}

	def getTrainingSet(self, fileName):
		#1. llegir corpus [paraula, tipus]
		#2. comptar quin tipus aparaiex mes cops
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
		
		self.generateModel(tags)
		

	def generateModel(self, tags):

		
		mostFreqTag = max(tags.iteritems(), key=operator.itemgetter(1))[0]
		file = open("lexic.txt", "w")
		file.write(mostFreqTag)

		dic = self.trainingSet.items()
		for word, tagValue in dic:
			tag, value = tagValue
			file.write( "\n" + word + "\t" + tag + "\t" + str(value) )

		file.close()
		return 0

class Prediction():

	def __init__ (self):
		self.testSet = []
		self.model = []

	def getTestModel(self, fileName):
		#1. llegir lexic.txt 
		#2. guardar en model [paraula, tipus, num]
		return 0
	def getTestSet(self, fileName):
		#1. llegir txt
		#2. guardar llista paraules
		return 0
	def tagging(self, fileName):
		#1. per cada paraula en testSet
		#1.1 si apareix a model
		#1.1.1 assignar tag
		#1.2 si no
		#1.2.a distancia
		#1.2.b mes frequent
		#2. escriure fitxer results.txt [paraula tipus]
		return 0
class Accuracy():

	def __init__ (self):
		self.solutions = []
		self.predictions = []

	def getSolutions(self, fileName):
		#1. llegir fitxer amb solucions i guardar [paraula, tipus]
		return 0
	def getPredictions(self, fileName):
		#1. llegir fitxer amb prediccions i guardar [paraula, tipus]
		return 0
	def computeAccuracy(self):
		#comparar solutions i predictions
		#prediccions correctes / num total
		#retornar accuracy
		return 0


class Main():
	#python tagger.py corpus.txt test.txt results.txt accuracy.txt
	model = TrainingModel()
	prediction = Prediction()
	accuracy = Accuracy()
	narg = len(sys.argv)
	corpus, test, result, solutions = "", "", "", ""

	if(narg != 5):
		#default
		corpus = "corpus.txt"
		test = "test_1.txt"
		result = "results.txt"
		solutions = "gold_standard_1.txt"
	else:
		corpus = sys.argv[1]
		test = sys.argv[2]
		result = sys.argv[3]
		solutions = sys.argv[4]

	model = TrainingModel()
	model.getTrainingSet(corpus)