import sys


class TrainingModel():

	def __init__ (self):
		self.trainingSet = {}

	def getTrainingSet(self, fileName):
		#1. llegir corpus [paraula, tipus]
		#2. comptar quin tipus aparaiex mes cops

		file = open(fileName)
		file2 = open("prova.txt", "w")
		lines = file.read().split("\r\n")
		#lines = lines.decode("latin_1").encode("UTF-8")
		for line in lines:
			if line == '':
				break
			line = line.decode("latin_1").encode("UTF-8")
			aux = line.split()
			self.trainingSet[aux[0]] = aux[1]
			
		print self.trainingSet
		file.close()
		file2.close()

	def generateModel(self):
		#2. guardar [paraula, tipus, num]
		#3. generar model (lexic.txt) (1A LINEA TIPUS MES FREQ) if(paraula ja existeix) then comparar num ...
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