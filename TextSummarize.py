#!/usr/bin/env python

'''
 I tried to implement Extractive Text Summarization.
 Basically count up the occurences of each word in the text. Then calculate its frequency
 according to the word that is occured the most. Then sum up the frequency of the words
 in each sentences. The sentence that has the highest frequency will be used as a summary
 of the text.

 resource:
	 http://glowingpython.blogspot.com/2014/09/text-summarization-with-nltk.html
	 The source code from the above url helped me to get started how to
	 compute the frequency and how I should rank the sentences.
'''

import re
import collections
from collections import defaultdict
from collections import Counter

class TextSummarize:

	def __init__(self):
		self.article = ''
		self.sentencesDictionary = {}
		self.wordCount = {}
		self.rankedSentence = ''

	def getArticle(self):
		text = self.article
		return text

	def setArticle(self, _article):
		self.article = _article

	def rankSentence(self, sentenceDict, wordList, wordWithFreqList):
		'''
		 This function rank the sentence according to the
		 total frequency of the words in the sentence.

		 This function will return a dictionary that contains
		 indexof the sentence with its total frequency

		 parameters:
		 	sentenceDict is dictionary that has a sentence with a index.
		 	wordList is a list that contains a list of words
		 	wordWithFreqList is dictionary that has word with the its frequency
		'''

		rankSentence = defaultdict(int)

		for index,sentence in sentenceDict.items():
			for word in wordList:
				tempSentList = sentence.split()
				if word in tempSentList:
					if word in wordWithFreqList:
						rankSentence[index] += wordWithFreqList[word]
					else:
						rankSentence[index] += 0

		return rankSentence

	def sentenceTokenize(self, article):
		'''
		 Tokenize the text into a sentence.
		 This function stores each sentence into a dictionary
		 with the index number.
		 Return: this function will return a dictionary
		 	ex. { 0: "This is sentence 0", 1: "This is sentence 1"}
		'''

		# regex pattern to match sentence
		regex = r"([\"]*[a-zA-z][a-z0-9A-Z, \-\'\"!<>\]\[]+[.][\"]*)"

		matches = re.findall(regex, self.article)

		for i,match in enumerate(matches):
			self.sentencesDictionary[i] = match

		# return a dictionary
		return self.sentencesDictionary

	def wordTokenize(self, sentences):
		'''
		 Tokenizes the words from sentences. This function will
		 count each words and calculate the frequency of the each words.
		 This function returns a dictionary, which contains the count of
		 the word and the word
		'''

		# we don't want to count up the frequent words that isn't important
		stopWords = ["to", "the", "a", "an", "of", "so", "in", "on", "not", "it", "is", "were", "are"]

		word = []

		#regex for word in a sentence
		regex = r"([a-zA-Z]+)"
		for s in sentences.values():
			matches = re.findall(regex, s.lower())
			for match in matches:
				if match not in stopWords:
					word.append(match)

		return word

	def computeWordFreq(self, wordList):

		# count the each word and store it into dictionary with its count
		d = {}
		for i in wordList:
			d[i] = d.get(i, 0) + 1

		# calculate the frequencies
		# get the largest value in the dictionary
		# and convert it to float
		maxVal = float(max(d.values()))

		'''
		Frequency normalization
			we want to ignore the frequeny of the word that is greater than 1.1
			becase in the case when "word word word ..." X 100
			this sentence doesn't have any meaning but it will have the highest
			frequency of all sentences.
		'''

		# we also want to ignore the word that is rarely shows up

		for key in d.keys():
			d[key] = d[key]/maxVal
			if d[key] >= 1.1:
				del d[key]
			elif d[key] <= 0.1:
				del d[key]

		# wordCount is a dictionary that contains word with its frequency
		self.wordCount = d
		return self.wordCount

	def displayRankedSentence(self, sentenceDict, sentenceWithFreq):
		'''
		 display first and second ranked the sentences
		 Parameter:
		 	sentenceDict contains sentence index and the sentence
		 	sentenceRank contains sentence index and the frequency from high to low
		'''

		# sorted ranked sentence list
		sentence_sorted = sorted(zip(sentenceWithFreq.values(), sentenceWithFreq.keys()))
		print sentence_sorted


		# if length of a list is greater than 4, then display the two sentences
		# with the highest frequencies
		# if length of a list is less than 4 but greater than 0, then display
		# the sentence with the highest frequency.
		firstSent = []
		secondSent = []
		if len(sentence_sorted) > 4:
			firstSent = sentence_sorted[-1]
			secondSent = sentence_sorted[-2]
			print "\n"
			print sentenceDict[firstSent[1]]
			print sentenceDict[secondSent[1]]
		elif ( (len(sentence_sorted) <= 3) and (len(sentence_sorted) > 0)):
			firstSent = sentence_sorted[-1]
			print "\n"
			print sentenceDict[firstSent[1]]
		else:
			print "Error"
			return


if __name__ == "__main__":

	'''
	 Get the text/article data from the database.
	'''

	article = raw_input()
	print ""

	#print article

	TS = TextSummarize()
	TS.setArticle(article)

	# matches is a dictionary ex { 0: "This is sentence 1", 1: "This is sentence 2"}
	matches = TS.sentenceTokenize(TS.getArticle())
	print "\nsentences: "
	print matches

	# wordList is a word list ex. ["a","b","c","d"]
	wordList = TS.wordTokenize(matches)
	print "\nword list: "
	print wordList

	# wordListWithFreq is a dictionary ex. { "a" : 0.5, "b": 1.0}
	wordListWithFreq = TS.computeWordFreq(wordList)
	print "\nword list with freq: "
	print wordListWithFreq

	#sentenceRank is a dictionary highest freq sentence to low ex. {0: 12.0, 1: 13.0}
	sentenceRank = TS.rankSentence(matches, wordList, wordListWithFreq)

	#display the first and second ranked sentence
	TS.displayRankedSentence(matches, sentenceRank)
