from math import *
import random
from game import NimState

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, state, move, parent=None):
        self.childNodes = []
        self.parent = parent
        self.visits = 0
        self.wins = 0
        self.move = move
        self.untried_moves = state.get_moves()
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


def UCT(rootstate, itermax, verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0].
    """
    rootnode = Node(state=rootstate)
    for i in range(itermax):
        node = rootnode
        state = rootstate.clone()
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

