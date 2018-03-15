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

class Classification():
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
			forbidden = ("?" , "!",'"', ",", ".", ";", ":")
			for s in  forbidden:
				if s =="." and re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", elem) != None:
					break;

  				elem =elem.replace(s,'')

			#if elem is not in forbidden:	
			elem = elem.lower()
			#afegim paraula amb valor 1 si el diccionari no la conte
			if not self.features.has_key(elem):
				self.features[elem] = 1

			#actualitzem valors
			else:
				self.features[elem]+= 1



	def toArffFormat(features):
		data = "% 1. Title: Classification\n" +
	    "% 2. Sources:\n"+
	    "% (a) Creator: Núria Rodríguez, Eva Valls\n\n"+
	    "@RELATION genre\n"
	    for elem in features	
	    	data += "@ATTRIBUTE "+elem +" STRING\n"
	   	
	    data+= "@ATTRIBUTE class        {female,male}"

class Main():

	#python tagger.py -t t1 -r results.txt 
	classification = Classification()
	features = classification.computeFeatures( "dataset" , 5, "words" )
	classification.toArffFormat(features)
	"""test, solutions, result = "filename", "gold_standard_1.txt", "results.txt"
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
	
    
    	punts extres -> calcular altres features com freq signes de puntuacio, etc
    	weka-> classify-> cross validation
	"""