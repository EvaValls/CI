import sys
import operator
import os
from string import punctuation
import re, itertools

class utils():

	def getInputFile(self, fileName):

		file = open(fileName)
		elements = file.read().split()
		file.close()
		return elements

	def parserWord(self, elem):
		#Busquem les paraules com a features
		forbidden = ("?" , "!",'"', ",", ".", ";", ":", "-", "'")
		for s in  forbidden:
			#Ignorar puntuacio d'un mail
			if s =="." and re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", elem) != None:
				break;
			#if s in elem:
			elem =elem.replace(s,'')		#Eliminar signes de puntuacio
		if elem ==" ":
			elem =elem.replace(" ",'')
		elem = elem.lower()						#Posar tot en miniscula
		return elem

	def parserPunctuation(self, elem):
		#Busquem els signes de puntuacio com a features
		punctuation = ("?" , "!",'"', ",", ".", ";", ":", "-", ".", "\xe2")
		
		for s in  punctuation:
			if s in elem:
				elem = s
			if s =="." and re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", elem) != None:
				break;

		if elem not in punctuation:
			elem =elem.replace(elem,'')
		
		return elem

	def writeFile(self, fileName, data):

		file = open(fileName, 'w')
		file.write(data)
		file.close()

class Extraction():
	def __init__ (self):
		self.features = {}

	def computeFeatures(self, dir, N,type):
		for filename in os.listdir(dir):
			self.featureExtraction(dir+'/'+filename, type)
		l = self.features.items()

		#Ordenem vector de features i retornem N primers
		lsorted = sorted(self.features, key=self.features.get, reverse=True)
		topN = lsorted[:N]
		return topN

	def featureExtraction(self, filename, type):
		
		for elem in utils().getInputFile(filename):
			#End of File
			if elem == '':
				break
			if type=="words":
				elem = utils().parserWord(elem)
			elif type == "punct":
				elem = utils().parserPunctuation(elem)
			
			if elem!="":
				if not self.features.has_key(elem):
					#Afegim paraula amb valor 1 si el diccionari no la conte
					self.features[elem] = 1
				else:
					#Actualitzem valors
					self.features[elem]+= 1

class Classifier():
	def __init__ (self, features):
		self.features = features
		self.data = ""

	def toArffFormat(self, type):
		#Escriure capcalera
		data = "% 1. Title: Classification\n% 2. Sources:\n% (a) Creator: Nuria Rodriguez, Eva Valls\n\n@RELATION genre\n"
		for elem in self.features:
			#Escriure cadascun dels features	
			if type== "punct":
				elem = "'"+elem+"'"
			data += "@ATTRIBUTE "+elem +" NUMERIC\n"
	   	
		data+= "@ATTRIBUTE class {female,male}\n@DATA\n"
		self.data = data

	def featureClassifier(self, dir, type):

		dictionary = {}
		self.toArffFormat(type)
		for f in self.features:
			#Inicialitzem diccionari
			dictionary[f] = 0

		for filename in os.listdir(dir):
			count = 0.0
			for elem in utils().getInputFile(dir+'/'+filename):
				if elem == '':
					break
				#Transformar elements al tipus de features
				if type == "words":
					elem = utils().parserWord(elem)
				elif type == "punct":
					elem = utils().parserPunctuation(elem)
				
				#Actualitzar vegades que apareix feature
				if elem!="":
					if dictionary.has_key(elem):
						dictionary[elem]+=1
					count += 1

			#Afegir una nova linia de data
			currentData = ""
			for f in self.features:
				if dictionary[f] == 0:
					currentData+= "?,"
				else :
					currentData += str(dictionary[f]/count) + ","
					dictionary[f] = 0
			if "female" in filename:
				currentData+= "female\n"
			else:
				currentData+= "male\n"
			self.data += currentData
		
		utils().writeFile("classifier.arff",self.data)


class Main():

	#python classification.py -n 100 -t word 

	N, type = 100, "words"
	i = 0
	for arg in sys.argv:
		if arg=="-n" :
			N = int(sys.argv[i+1])
		if arg=="-t":
			type = sys.argv[i+1]
		i+=1

	extraction = Extraction()
	features = extraction.computeFeatures( "dataset" , N, type )

	classifier = Classifier(features)
	classifier.featureClassifier("dataset", type)
