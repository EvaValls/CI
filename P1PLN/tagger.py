import sys

class Main(argv):
	#python tagger.py corpus.txt test.txt results.txt accuracy.txt
	model = TrainingModel()
	prediction = Prediction()
	accuracy = Accuracy()
	narg = len(sys.argv)
	corpus, test, result, solutions = ""

	if(narg != 5):
		#default
		corpus = "corpus.txt"
		test = "test_1.txt"
		result = "results.txt"
		solutions = "gold_standard_1.txt"
	else:
		corpus = sys.arv[1]
		test = sys.arv[2]
		result = sys.arv[3]
		solutions = sys.arv[4]

	


class TrainingModel():

	def __init__ (self):
		self.trainingSet = []

	def getTrainingSet(self, fileName):
		#1. llegir corpus [paraula, tipus]
		#2. comptar quin tipus aparaiex mes cops
		file = open(fileName)
		lines = file.split("\n\r")
		for line in lines:
			aux = line.split("\t")
			self.trainingSet.append(aux)
		print self.trainingSet

	def generateModel(self):
		#2. guardar [paraula, tipus, num]
		#3. generar model (lexic.txt) (1A LINEA TIPUS MES FREQ) if(paraula ja existeix) then comparar num ...

class Prediction():

	def __init__ (self):
		self.testSet = []
		self.model = []

	def getTestModel(self, fileName):
		#1. llegir lexic.txt 
		#2. guardar en model [paraula, tipus, num]

	def getTestSet(self, fileName):
		#1. llegir txt
		#2. guardar llista paraules

	def tagging(self, fileName):
		#1. per cada paraula en testSet
		#1.1 si apareix a model
		#1.1.1 assignar tag
		#1.2 si no
		#1.2.a distancia
		#1.2.b mes frequent
		#2. escriure fitxer results.txt [paraula tipus]

class Accuracy():

	def __init__ (self):
		self.solutions = []
		self.predictions = []

	def getSolutions(self, fileName):
		#1. llegir fitxer amb solucions i guardar [paraula, tipus]

	def getPredictions(self, fileName):
		#1. llegir fitxer amb prediccions i guardar [paraula, tipus]

	def computeAccuracy(self):
		#comparar solutions i predictions
		#prediccions correctes / num total
		#retornar accuracy
