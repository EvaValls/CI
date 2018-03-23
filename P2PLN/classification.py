import sys
import operator
import os
from string import punctuation
import re, itertools

class utils():

	def getInputFile(self, fileName):

		file = open(fileName)
		lines = file.read().split()
		file.close()

		return lines	
	def parserWord(self, elem):
		forbidden = ("?" , "!",'"', ",", ".", ";", ":", "-", "'")
		for s in  forbidden:
			if s =="." and re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", elem) != None:
				break;

			elem =elem.replace(s,'')
		if elem ==" ":
			elem =elem.replace(" ",'')
			#if elem is not in forbidden:	
		elem = elem.lower()
		return elem

	def parserPunctuation(self, elem):
		punctuation = ("?" , "!",'"', ",", ".", ";", ":", "-")
		
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

	
		lsorted = sorted(self.features, key=self.features.get, reverse=True)
		topN = lsorted[:N]
		return topN

	def featureExtraction(self, filename, type):
		
		for elem in utils().getInputFile(filename):
			#End of File
			if elem == '':
				break
			if type=="word":
				elem = utils().parserWord(elem)
			elif type == "punct":
				elem = utils().parserPunctuation(elem)
			#afegim paraula amb valor 1 si el diccionari no la conte
			if elem!="":
				if not self.features.has_key(elem):
					if elem !="":
						self.features[elem] = 1

				#actualitzem valors
				else:
					self.features[elem]+= 1

class Classifier():
	def __init__ (self, features):
		self.features = features
		self.data = ""

	def toArffFormat(self, type):
		data = "% 1. Title: Classification\n% 2. Sources:\n% (a) Creator: Nuria Rodriguez, Eva Valls\n\n@RELATION genre\n"
		for elem in self.features:	
			if type== "punct":
				elem = "'"+elem+"'"
			data += "@ATTRIBUTE "+elem +" NUMERIC\n"
	   	
		data+= "@ATTRIBUTE class {female,male}\n@DATA\n"
		self.data = data
	def featureClassifier(self, dir, type):
		dictionary = {}
		
		self.toArffFormat(type)
		for f in self.features:
				dictionary[f] = 0

		for filename in os.listdir(dir):
			count = 0.0
			for elem in utils().getInputFile(dir+'/'+filename):
				if elem == '':
					break
				if type == "word":
					elem = utils().parserWord(elem)
				elif type == "punct":
					elem = utils().parserPunctuation(elem)
				if elem!="":
					if dictionary.has_key(elem):
						dictionary[elem]+=1
					count += 1
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

	N, type = 100, "word"
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
