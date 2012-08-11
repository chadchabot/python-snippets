import sys
import re

class Counter(dict):
    def __missing__(self, key):
        return 0

def buildWord2( dictWord, letterLookupTable ):
    #    new approach to the buildWord() function
    letterCount = Counter()
    for letter in dictWord:
        letterCount[ letter ] += 1
    
    for letter in letterCount:
        if ( letterLookupTable[ letter ] < letterCount[ letter ] ):
            return 0
        else:
            return 1
        



def buildWord( stringToMatch, letterLookupTable ):

    for letter in stringToMatch:
        #   new copy of letterLookupTable
        table = Counter()
        for key in letterLookupTable:
            table[ key ] = letterLookupTable[ key ]
        #   if the letter is found in table
        if ( letter in table ):
            if ( table[ letter ] > 0 ):
                #   decrement value of table[letter]
                table[ letter ] -= 1
            else:
                print str( letter ) + " = " + str( table[ letter ] )
        else:
            return 0
    print stringToMatch + "\t -- " + str( table )
    return 1

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
        sys.exit( 1 )

    string = sys.argv[ 1 ]
    if not string:
        sys.exit( 1 )

    #   check for any non-alpha characters in input
    digitFound = re.search( "\d", string )
    if digitFound:
        print "\tA character that is not a letter was found.\n\tPlease don't use numbers or any weird stuff like that."
        sys.exit( 1 )

    #   build player hand
    playerHand = Counter()
    playerHandLength = len( string )
    for letter in string:
        #   add to lookup table
        playerHand[ letter ] += 1
    
#    for key in playerHand:
#        print key + " = " + str( playerHand[ key ] )

    #   load dictionary file
    with open( "/usr/share/dict/words" ) as fp:
        dict_file = fp.readlines()
    
    #   need a place to store words that can be made from input string
    wordList = []
    print "\t -- " + str( playerHand )
    #   go through each word in the dict file
    for word in dict_file:
        #   trim the newline character
        word = word[:-1]
        #   is 'word' longer than the length of input string?
        #   can this check be combined with the readlines() or dict_file building step?
        #   use a system call (grep?) and pipe results to dict_file?
        if ( len( word ) <= playerHandLength ):
            #   check if 'word' can be built using 'playerHand'
            if ( 1 == buildWord2( word, playerHand ) ):
                #   add to wordList
                wordList.append( word )
    
#    print wordList
    #   check for longest word
    longest = longestWord( wordList )
    
    print "The longest word(s) to be made given [" + string + "]:"
    for word in longest:
        print word
        

if __name__ == '__main__':
    main()