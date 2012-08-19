import sys
import re

class Counter( dict ):
    def __missing__( self, key ):
        return 0
    def __keyerror__( self, key ):
        print "no entry for [" + key + "]"
        return 0

def testWord( dictWord, letterLookupTable ):
    #   for each letter in dictWord, add to a dictionary
    letterCount = Counter()
    blanksRequired = 0
    for letter in dictWord:
        if letter in letterLookupTable:
            letterCount[ letter ] += 1
            if ( letterLookupTable[ letter ] < letterCount[ letter ] ):
                return 0
        else:
            if blanksRequired < letterLookupTable[ '?' ]:
                blanksRequired += 1
            else:
                return 0
    return 1

def calculateScore( word ):
    """  
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

def buildPlayerHand( playerTiles ):
    playerHand = Counter()
    playerHand.clear()
    for letter in playerTiles:
        #   add to lookup table
        playerHand[ letter ] += 1
    return playerHand

def longestWord( wordList ):
    length = 0
    longestWord = []
    
    for word in wordList:
        #   here is where I would add in a calculator for word value
        wordLength = len( word )
        if ( wordLength == length ):
            #   add to list
            longestWord.append( word )
        elif ( wordLength > length ):
            del longestWord[:]
            length = len( word )
            longestWord.append( word )

    return longestWord

def main():
    if ( len( sys.argv ) < 2 ):
        print "\tYou need to supply an input string"
        sys.exit( 1 )

    string = sys.argv[ 1 ].lower()
    if not string:
        sys.exit( 1 )

    #   check for any non-alpha characters in input
    digitFound = re.search( "\d", string )
    if digitFound:
        print "\tA character that is not a letter was found.\n\tPlease don't use numbers or any weird stuff like that."
        sys.exit( 1 )

    #   build player hand
    playerHand = buildPlayerHand( string )
    playerHandLength = len( string )
    
    for key in playerHand:
        print key + " = " + str( playerHand[ key ] )
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
            if ( 1 == testWord( word, playerHand ) ):
                #   add to wordList
                wordList[ word ] = calculateScore( word.lower() )
    
#    print wordList
    #   check for longest word
    longest = longestWord( wordList )
    
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