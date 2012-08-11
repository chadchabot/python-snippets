import sys
import re

def buildWord( stringToMatch, letterLookupTable ):

    for letter in stringToMatch:
        #   new copy of letterLookupTable
        table = {}
        for key in letterLookupTable:
            table[ key ] = letterLookupTable[ key ]
        #   if the letter is found in table
        if ( letter in table ):
            #   decrement value of table[letter]
            table[ letter ] -= 1
            #   if table[value] == 0
            if ( table[ letter ] == 0 ):
                del table[ letter ]
        else:
            return 0
    
    return 1


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
    playerHand = {}
    playerHandLength = len( string )
    for letter in string:
        #   add to lookup table
        if ( letter in playerHand ):
            playerHand[ letter ] += 1
        else:
            playerHand[ letter ] = 1
    
    for key in playerHand:
        print key + " = " + str( playerHand[ key ] )

    #   load dictionary file
    with open( "/usr/share/dict/words" ) as fp:
        dict_file = fp.readlines()
    
    #   need a place to store words that can be made from input string
    wordList = []

    #   go through each word in the dict file
    for word in dict_file:
        #   trim the newline character
        word = word[:-1]
        #   is 'word' longer than the length of input string?
        #   can this check be combined with the readlines() or dict_file building step?
        #   use a system call (grep?) and pipe results to dict_file?
        if ( len( word ) <= playerHandLength ):
            #   check if 'word' can be built using 'playerHand'
            if ( 1 == buildWord( word, playerHand ) ):
                #   add to wordList
                wordList.append( word )
    
    print wordList
        

if __name__ == '__main__':
    main()