"""
Babbleturm version 0.0
a script for making conlangs

Usage:
python babbleturm.py <output_filename>
"""

import string
import sys
import time

import random
import codecs

output_filename = 'babbleturm_words.txt'
output_line_format = '%s\n'

if len(sys.argv) >= 2:
    if sys.argv[1] == '--help':
        print __doc__
        sys.exit(0)
    else:
        output_filename = sys.argv[1]
        print "output file is ", output_filename


def choice_weighted(weights):
    scores = {}
    for choice, weight in weights.items():
        scores[random.randint(0,weight)] = choice
    winning_score = max(scores.keys())
    return scores[winning_score]
    


class LanguageSeed(object):
    def __init__(_, num_syllables=200):
        random.seed(time.time())

        _.either.extend([l for l in string.ascii_lowercase if l not in _.vowels])
        map(_.either.remove, _.exclude)

        _.initials.extend(_.either)
        _.finals.extend(_.either)

        trash = []

        for letter in _.vowels:
            try:
                true_letter = _.orthography[letter]
                trash.append(letter)
                _.vowels.append(true_letter)
            except KeyError:
                pass
        map(_.vowels.remove, trash)

        _.syllables = set([_.makeSyllable() for i in range(0, num_syllables)])


    def makeWord(_, num_syllables=None):
        syllables = list(_.syllables)
        if num_syllables is None:
            num_syllables = choice_weighted(_.syllable_sizes)

        word = ''
        for i in range(0, num_syllables):
            word += random.choice(syllables)

        return word


    def makeSyllable(_):
        initial = ''
        final = ''

        if random.random() < _.morpheme_chance['initial']:
            initial = random.choice(_.initials)
        if random.random() < _.morpheme_chance['final']:
            final = random.choice(_.finals)

        return unicode(initial + random.choice(_.vowels) + final)


    def printReport(_):
        print "vowels..."
        print `_.vowels`
    
        print "consonants..."
        print `_.either`

        print "syllables..."
        print `_.syllables`

        print "\nExample text:"
        for i in range(0, 40):
            print _.makeWord(),
    
        print "\n... done!\n"



class Geirmannik(LanguageSeed):
    vowels = ['a', 'e', 'i', 'o', 'u', 'y',
        'aa', 'ai', 'ie', 'ei', 'eu', 'ue', 'oe', 'ae', 'ui', 'iu', 'yy']


    #initials = [ 'ts', 'sh', 'ch', 'tj', 'dj', 'dz', 'hr', 'sv' ]
    #finals = [ 'nt', 'rt', 's', 'z', 'ht' ]
    initials = [ 'hr', 'sv', 'kj' ]
    finals = [ 'nt', 'rt', 'ht', 'ng', 'k', 'ks', 'ss', 'ml', 'ln', 'll' ]
    either = [ 'th', 'sj', ]

    exclude = ['w','x','c','q']
    
    morpheme_chance = {
        'initial' : 0.8,
        'final' : 1,#0.7,
    }

    syllable_sizes = {
        1 : 15,
        2 : 20,
        3 : 5,
    }

    orthography = {
      'aa' : u'\u00e5',
      'ae' : u'\u00e4',
      'oe' : u'\u00f6',
      'ue' : u'\u00fc',
      'ii' : u'\u00ef',
      #'oo' : u'\u00d4',
    }


class German(LanguageSeed):
    vowels = ['a', 'e', 'i', 'o', 'u',
        'ai', 'ia', 'ie', 'ei', 'eu', 'ue', 'oe', 'ae', 'oo', 'ee']

    initials = [ 'dj', 'pf' ]
    finals = [ 'nt', 'nn', 'rt', 'hrt', 'ng', 'ck', 'cks' ]
    either = [ 'th', 'sch', 'ch', 'tsch' ]

    exclude = ['x','y','c','q']

    syllable_sizes = {
        1 : 10,
        2 : 20,
        3 : 5,
    }

    morpheme_chance = {
        'initial' : 0.8,
        'final' : 1,#0.7,
    }

    orthography = {
      'ae' : u'\u00e4',
      'oe' : u'\u00f6',
      'ue' : u'\u00fc',
    }



def main():
    mundart = Geirmannik()
    #mundart = German()

    mundart.printReport()

    final_words = set()
    decision = 'y'
    print "==== Constructing dictionary ===="
    decision = raw_input("Want to choose which words to approve?")
    if decision.lower() == 'y':
        while decision.lower() in ('y', 'n'):
            new_word = mundart.makeWord()
            print new_word, " \t\tAccept word? (Yes/No/Save+quit/Quit):",
            decision = raw_input()
            if decision in ('y', 'Y'):
                final_words.add(new_word)
    else:
        final_words = set([mundart.makeWord() for i in range(0,500)])

    if decision in ('q', 'Q'):
        print "Quit witout saving."
    else:
        fh = codecs.open(output_filename, 'a', 'utf-8')
        for w in final_words:
            fh.write(output_line_format % w)
        fh.close()
        print "Written to file '%s'." % output_filename


if __name__ == '__main__':
    main()


