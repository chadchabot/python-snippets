import sys

#   for letter in string

def main():
    if ( len( sys.argv ) < 2 ):
        sys.exit( 1 )

    string = sys.argv[ 1 ]
    if not string:
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

    

if __name__ == '__main__':
    main()