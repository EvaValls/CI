import sys
import operator

class TrainingModel():

	def __init__ (self):
		self.trainingSet = {}

	def getTrainingSet(self, fileName):
		#1. llegir corpus [paraula, tipus]
		#2. comptar quin tipus aparaiex mes cops
		tags = {}
		file = open(fileName)
		lines = file.read().split("\r\n")
		for line in lines:
			#End of File
			if line == '':
				break

			line = line.decode("latin_1").encode("UTF-8")
			aux = line.split()

			#actualitzar vegades que apareix paraula-tag
			if self.trainingSet.has_key((aux[0],aux[1])) :
				self.trainingSet[(aux[0],aux[1])] = self.trainingSet[(aux[0],aux[1])]+1
			else:
				self.trainingSet[(aux[0],aux[1])] = 1

			#actualitzar vegades que apareix un tag
			if tags.has_key(aux[1]) :
				tags[aux[1]] = tags[aux[1]] + 1
			else:
				tags[aux[1]] = 1

		print tags

		file.close()
		self.generateModel(tags)
		

	def generateModel(self, tags):

		
		mostFreq = max(tags.iteritems(), key=operator.itemgetter(1))[0]
		file = open("lexic.txt", "w")
		file.write(mostFreq)

		words, tags, values = [], [], []

		"""dic = self.trainingSet.items()
		for tupla,value in dic:
			word, tag = tupla
			if word not in words:
				words.append(word)
				tags.append(tag)
				values.append(value)
			else:
				index = words.index(word)
				if values[index] < value :
					tags[index] = tag
					values[index] = value

		for i in range(len(words)):
			file.write(words[i]+"\t"+tags[i]+"\t"+values[i])"""

		"""for tupla, value in dic:
			word, tag = tupla
			if any(k[0] == word for k in dic):"""



		file.close()


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