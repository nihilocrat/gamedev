#!/bin/python
import random

class FairDice(object):
    """
    These 'dice' implement the probability mechanics described by Sid Meier and Rob Pardo at GDC 2010.
    see: http://www.shacknews.com/featuredarticle.x?id=1302
    
    They are meant to be more 'fair' than normal probability, following natural language.
    If '5 times out of 10' you want something to happen, call 'dict = FairDice(5,10)'.
    If you call 'dice.roll()' 5 times, it will absolutely return True by the 5th time, if not sooner.
    
    Set "linear" to False if you want it to work precisely this way. Otherwise, it will become slightly more likely to return True with each roll.
    """
    tries = 0
    chances = (1.0,10.0)
    history = []
    linear = True
    
    def __init__(self, times, outof):
        """
        "x times out of y", these dice will return true when roll() is called
        
        @param times: "x times..."
        @param outof: "out of y", this must be greater than 0
        """
        self.chances = (float(times), float(outof))
    
    def roll(self):
        """
        @return: True or False
        """
        if self.linear:
            base_prob = (self.chances[0] + self.tries) / self.chances[1]
        else:
            base_prob = self.chances[0] / self.chances[1]
        
        if random.random() < base_prob:
            # FIXME : no history for now... can't think of a good way to implement it
            #self.history.append(self.tries)
            self.reset()
            return True
        else:
            self.tries += 1
            return False        
    
    def reset(self):
        """
        Reset the dice so that the next roll will be treated as the first in a series.
        """
        self.tries = 0

        