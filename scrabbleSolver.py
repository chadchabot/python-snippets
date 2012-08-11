import sys
import re

#   for letter in string

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
    for letter in string:
        #   add to lookup table
        if ( letter in playerHand ):
            playerHand[ letter ] += 1
        else:
            playerHand[ letter ] = 1
    
    for key in playerHand:
        print key + " = " + str( playerHand[ key ] )

    #   load dictionary file
    

if __name__ == '__main__':
    main()