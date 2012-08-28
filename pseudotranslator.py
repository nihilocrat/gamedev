# Pseudotranslator
#
# Input : wordlist from psueodlanguage (.txt), sample text in a real language (.txt), real-to-pseudolanguage dictionary filename
# Output : verbatim "translation" of sample text into the pseudolanguage, dictionary (JSON) written to filename

# Pseudocode:
#
# Read in english text passage
# For each word, check to see if it's in our dictionary and add it to the output text
## if not, go to our wordlist and find a word with a similar length
## (for each three letters in the source word, allow +/- 1 letter, +1, so a 6-letter word could be +/- 3)
## then remove this from the wordlist
## insert this word in our dictionary
# print output text
# convert dictionary to JSON
# write JSON to given filename

import sys
import re
import random
import json

usage = """ Input : wordlist from psueodlanguage (.txt), sample text in a real language (.txt), real-to-pseudolanguage dictionary filename """
try:
    scriptname, wordlistFilename, sampleFilename, dictionaryFilename = sys.argv
except ValueError:
    print usage
    sys.exit(0)

dictionary = {}
wordlist = []
output = "\n"

def flatten(seq):
      """
      Flatten a nested list
      ex: [1, [2, 3], 4] to [1, 2, 3, 4]
      """
      lst = []
      for el in seq:
        if getattr(el, '__iter__', False):
          lst.extend(flatten(el))
        else:
          lst.append(el)
      return lst

fh = open(wordlistFilename, "r")
textlines = [line.split() for line in fh.readlines()]
wordlist = flatten(textlines)
wordlist = [word.lower() for word in wordlist]
fh.close()

sortedWordList = {}
longestWordLength = 0
for word in wordlist:
    l = len(word)
    if l > longestWordLength:
        longestWordLength = l
    if not sortedWordList.has_key(l):
        sortedWordList[l] = []
    sortedWordList[l].append(word)
    
def GetNewPseudoWord(word):
    # search wordlist for similar-sized word
    wordlength = len(word)
    variance = int(wordlength/3) + 1
    wordlength += random.randrange(-variance, variance)
    if wordlength < 1:
        wordlength = 1
    if wordlength > longestWordLength:
        wordlength = longestWordLength
    
    try:
        possibleWords = sortedWordList[wordlength]
        newPseudoWord = random.choice(possibleWords)
    except (KeyError, IndexError):
        # no more words of that length!
        # try again!
        return "(blorp)" #return GetNewPseudoWord(word)
    
    # remove from list of possible words
    sortedWordList[wordlength].remove(newPseudoWord)
    
    return newPseudoWord
    
    
fh = open(sampleFilename, "r")
for line in fh.readlines():
    for word in line.split():
        # leave numbers alone
        try:
            wordNumber = int(word)
            wordNumber = float(word)
            continue
        except ValueError:
            pass
        
        word = re.sub(r"[\"',.\?\!;:\(\)\[\]0-9]", " ", word)
        word = word.lower()
        word = word.strip()
        if not dictionary.has_key(word):
            newPseudoWord = GetNewPseudoWord(word)
            
            dictionary[word] = newPseudoWord
        
        output += dictionary[word] + " "

    output += "\n"
		
fh.close()

#dictionaryText = json.dumps(dictionary)
import pprint
dictionaryText = pprint.pformat(dictionary)
fh = open(dictionaryFilename, "w")
fh.write( dictionaryText )
fh.close()

print output