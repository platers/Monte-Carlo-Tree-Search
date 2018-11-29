from math import *
import random
from game import *

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, state, move=None, parent=None):
        self.childNodes = []
        self.parent = parent
        self.visits = 0
        self.wins = 0
        self.move = move
        self.untried_moves = state.GetMoves()
        self.playerJustMoved = state.playerJustMoved

    def select(self):
        node = max(self.childNodes, key=lambda x: x.UCB())
        return node

    def UCB(self):
        return self.wins / self.visits + sqrt(log(self.parent.visits) / self.visits)

    def add_child(self, move, state):
        node = Node(state, move, self)
        self.untried_moves.remove(move)
        self.childNodes.append(node)
        return node

    def update(self, result):
        self.visits += 1
        self.wins += result #this is from viewpoint of playerJustMoved

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(
            self.untriedMoves) + "]"

def UCT(rootstate, itermax, verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0].
    """
    rootnode = Node(state=rootstate)
    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()
        #selection
        while node.untried_moves == [] and node.childNodes != []:
            node = node.select()
            state.DoMove(node.move)

        #expansion
        if node.untried_moves != []:
            m = random.choice(node.untried_moves)
            state.DoMove(m)
            node = node.add_child(m, state)

        #simulation
        while state.GetMoves() != []:
            state.DoMove(random.choice(state.GetMoves()))

        #backpropogation
        while node != None:
            node.update(state.GetResult(node.playerJustMoved))
            node = node.parent

    return sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move

def UCTPlayGame():
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    # state = OthelloState(4) # uncomment to play Othello on a square board of the given size
    state = OXOState() # uncomment to play OXO
    #state = NimState(15) # uncomment to play Nim with the given number of starting chips
    while (state.GetMoves() != []):
        print(str(state))
        if state.playerJustMoved == 1:
            m = UCT(rootstate = state, itermax = 1000, verbose = False) # play with values for itermax and verbose = True
        else:
            m = UCT(rootstate = state, itermax = 10, verbose = False)
        print("Best Move: " + str(m) + "\n")
        state.DoMove(m)
    if state.GetResult(state.playerJustMoved) == 1.0:
        print("Player " + str(state.playerJustMoved) + " wins!")
    elif state.GetResult(state.playerJustMoved) == 0.0:
        print("Player " + str(3 - state.playerJustMoved) + " wins!")
    else: print("Nobody wins!")

if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players. 
    """
    UCTPlayGame()