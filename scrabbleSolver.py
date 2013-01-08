#!/usr/bin/python
#Copyright 2012 Chad Chabot
#
#chad@chadchabot.com
#github.com/chadchabot

import sys
import re
from pydoc import help

class Counter( dict ):
    """
    Counter is an extension of the dict class, where keys that are not
    found in the dict will not return an error, but will return a value of 0.
    The error message should be re-directed towards an error log.
    """

    def __missing__( self, key ):
        #print "missing key error for [" + key + "]"
        return 0
    def __keyerror__( self, key ):
        #print "key error for [" + key + "]"
        return 0


def testWord( dictWord, letterLookupTable, must_includes ):
    """
    testWord() checks to see if 'dictWord' can be created using the contents
    of 'letterLookupTable'.
    
    Parameters:
        dictWord
            A string of arbitrary size.
        
        letterLookupTable
            A Counter object containing a tally of the letters in the player's
            hand.
    
    
    The testWord() function compares a word from a dictionary or other source
    (the 'dictWord' param) against a supplied lookup table (a Counter object)
    containing from the tiles in the player's hand ('letterLookupTable' param).

    If 'dictWord' can be formed using the letters in 'letterLookupTable',
    testWord() returns the value of the word, according to the point
    distribution defined in calculateScore().
    
    If 'dictWord' cannot be formed, testWord() returns -1.
    """
    #   for each letter in dictWord, add to a dictionary
    letterCount = Counter()
    bonusValue = 50
    blanksRequired = 0
    wordScore = 0
    
    for letter in must_includes:
        if (dictWord.find( letter ) == -1):
            return -1
    
    for letter in dictWord:
        if letter in letterLookupTable:
            letterCount[ letter ] += 1
            if ( letterLookupTable[ letter ] < letterCount[ letter ] ):
                return -1
            else:
                wordScore += calculateScore( letter )
        else:
            if blanksRequired < letterLookupTable[ '?' ]:
                blanksRequired += 1
            else:
                return -1

    #   if giving the player a bonus for using all 7 tiles, use the return below
    #return wordScore if len( dictWord ) != 7 else wordScore + bonusValue
    return wordScore


def calculateScore( word ):
    """
    calculateScore() totals the point value of the parameter 'word'.
    
    parameters:
        word
            a string or single character, made up of alpha characters and
            question marks ["?"]
            
    
    reference for point values
    https://en.wikipedia.org/wiki/Scrabble_letter_distributions
    """
    scoreTable = ( {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2,
                    'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
                    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1,
                    'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10 } )

#    for key in scoreTable:
#        print str( key ) + " = " + str( scoreTable[ key ] )

    wordScore = 0
    for letter in word:
        wordScore += scoreTable[ letter ]
    
    return wordScore

def buildPlayerHand( playerTiles, must_includes ):
    """
    buildPlayerHand() populates and returns a Counter based on the supplied string.
    
    Parameters:
        playerTiles
            A string consisting of letters and/or question marks (provided the
            string has already been checked for valid characters).
    
    Return:
        playerHand, the tally of letters contained in 'playerTiles'.
    """
    
    playerHand = Counter()
    playerHand.clear()
    for letter in playerTiles:
        #   add to lookup table
        playerHand[ letter ] += 1
    
    for letter in must_includes:
        playerHand[ letter ] += 1

    return playerHand

def findLongestWord( wordList ):
    """
    findLongestWord() takes in a list of words and returns the longest, or a list
    containing the longest words.
    
    Parameters:
        wordList
            an unordered list of words.
    
    Return:
        'longestWord' an array of the longest words in 'wordList'.
    """
    length = 0
    longestWord = []
    
    for word in wordList:
        wordLength = len( word )
        if ( wordLength == length ):
            #   add to list
            longestWord.append( word )
        elif ( wordLength > length ):
            del longestWord[:]
            length = len( word )
            longestWord.append( word )

    return longestWord

def validateInput( string ):
    badCharacterFound = re.search("[^a-zA-Z?]", string )
    return True if badCharacterFound else False

def main():
    if ( len( sys.argv ) < 2 ):
        print "\tYou need to supply an input string"
        sys.exit( 1 )

    #   what about a flag to show all/some/limited number of results, not just top?

    string = sys.argv[ 1 ].lower()
    if not string:
        sys.exit( 1 )

    must_includes = ''
    if ( len( sys.argv ) == 3):
        must_includes = sys.argv[ 2 ].lower()
        
    #   check for any non-alpha characters in input
    if validateInput( string ):
        print "\tA character that is not a letter was found.\n\tPlease don't use numbers or any weird stuff like that."
        sys.exit( 1 )

    #   build player hand
    playerHand = buildPlayerHand( string, must_includes )
    playerHandLength = len( string )
    
#    for key in playerHand:
#        print key + " = " + str( playerHand[ key ] )
#    print "\t -- " + str( playerHand )

    #   load dictionary file
    with open( "/usr/share/dict/words" ) as fp:
        dict_file = fp.readlines()
    
    #   need a place to store words that can be made from input string
    wordList = Counter()

    #   go through each word in the dict file
    for word in dict_file:
        #   trim the newline character
        word = word[:-1]
        #   is 'word' longer than the length of input string?
        """
            Can this check be combined with the readlines() or dict_file building step?
            Use a system call (grep?) and pipe results to dict_file?
            If the script is a "run once and quit", this is an acceptable approach.
            If the script has a longer life/persistance, then all words must be loaded
        """
        if ( len( word ) <= playerHandLength ):
            #   check if 'word' can be built using 'playerHand'
            wordScore = testWord( word, playerHand, must_includes )
            if ( -1 != wordScore ):
                #   add to wordList
                wordList[ word ] = wordScore
    
    #print wordList
    #   check for longest word
    longest = findLongestWord( wordList )
    
    print "The longest word(s) to be made given [" + string + "]:"
    for word in longest:
        print "'" + str( word ) + "' is worth " + str( wordList[ word ] )+ " points"

    highestValue = 0
    print "The highest scoring words that can be made from [%s] are:" % string
    for key, value in sorted( wordList.iteritems(), key=lambda ( k,v ): ( v, k ), reverse=True ):
        if value > highestValue:
            highestValue = value
        if value == highestValue:
            print "'%s' is worth %s points" % ( key, value )

if __name__ == '__main__':
    main()