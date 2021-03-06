import sys

# Checks the usage in the command line
if len(sys.argv) != 2:
    print "Usage: python bricks.py <num_bricks>"
    sys.exit(0)

# get the starting number of bricks
bricks = int(sys.argv[1])

# ------- create the NuSMV code ----------- #

linebreak = lambda a,b: a+"\n"+b

# module declaration and variable declaration
main = """MODULE main
VAR
    bricks : 0..{0}; 
    i : 1..3;
    j : 1..3;
    turn : boolean;
    winner : {{none, a, b}};
ASSIGN""".format(bricks)

#TODO the initialization of variables
init = """
	init(bricks) := {0};
	init(turn) := TRUE;
	init(winner) := none;
""".format(bricks)


#TODO transitions
next = """
	next(turn) := case
					bricks > 0: !turn;
					TRUE	: turn;
				esac;
	next(bricks) := case
						bricks >= 3	: bricks - i;
						bricks = 2	: {0 , 1};
						bricks = 1	: 0;
						TRUE	: 0;
					esac;

	next(winner) := case
						bricks > 0	: none;
						bricks = 0	: winner = none ? (turn ? a : b) : winner;
						TRUE	: winner;
					esac;
"""


#TODO the specifications 
spec = """
SPEC AF (winner = a | winner = b);
SPEC AF ((AG winner = a) | (AG winner = b));
SPEC EF (turn = FALSE -> AG winner = a)
"""

# put it all together
print reduce(linebreak, [main,init,next,spec])

