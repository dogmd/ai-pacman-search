# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]    

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    steps = util.Stack()
    # Store (state, action, cost), and parent
    steps.push([(problem.getStartState(), None, 0), None])
    seenStates = [problem.getStartState()]

    while not steps.isEmpty():
        step = steps.pop()
        state = step[0][0]
        seenStates.append(state)
        if problem.isGoalState(state):
            actions = []
            # Backtrack through parents to get actions
            while step:
                actions.insert(0, step[0][1])
                step = step[1]
            return actions[1:]
        
        successors = problem.getSuccessors(state)
        for successor in successors:
            newState = successor[0]
            if newState not in seenStates:
                steps.push([successor, step])

    # Goal not found
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    steps = util.Queue()
    # Store (state, action, cost), and parent
    steps.push([(problem.getStartState(), None, 0), None])
    seenStates = [problem.getStartState()]

    while not steps.isEmpty():
        step = steps.pop()
        state = step[0][0]
        seenStates.append(state)
        if problem.isGoalState(state):
            
            actions = []
            # Backtrack through parents to get actions
            while step:
                actions.insert(0, step[0][1])
                step = step[1]
            return actions[1:]
        
        successors = problem.getSuccessors(state)
        for successor in successors:
            newState = successor[0]
            if newState not in seenStates:
                seenStates.append(newState)
                steps.push([successor, step])

    # Goal not found
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    steps = util.PriorityQueue()
    # Store (state, action, cost), and parent
    steps.push([(problem.getStartState(), None, 0), None], 0)
    seenStates = {problem.getStartState(): 0}

    while not steps.isEmpty():
        step = steps.pop()
        state = step[0][0]
        seenStates[state] = step[0][2]
        if problem.isGoalState(state):
            actions = []
            # Backtrack through parents to get actions
            while step:
                actions.insert(0, step[0][1])
                step = step[1]
            return actions[1:]
        
        successors = problem.getSuccessors(state)
        for successor in successors:
            newState = successor[0]
            totalCost = successor[2] + step[0][2]
            if newState not in seenStates or seenStates[newState] > totalCost:       
                seenStates[newState] = totalCost
                steps.push([(newState, successor[1], totalCost), step], totalCost)

    # Goal not found
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    steps = util.PriorityQueue()
    # Store (state, action, cost), and parent
    startState = problem.getStartState()
    steps.push([(problem.getStartState(), None, heuristic(startState, problem)), None], heuristic(startState, problem))
    seenStates = {problem.getStartState(): 0}

    while not steps.isEmpty():
        step = steps.pop()
        state = step[0][0]
        seenStates[state] = step[0][2]
        if problem.isGoalState(state):
            actions = []
            # Backtrack through parents to get actions
            while step:
                actions.insert(0, step[0][1])
                step = step[1]
            return actions[1:]
        
        successors = problem.getSuccessors(state)
        for successor in successors:
            newState = successor[0]
            pathCost = step[0][2] + successor[2]
            estimatedCost = heuristic(newState, problem) + pathCost
            if newState not in seenStates or seenStates[newState] > pathCost:       
                seenStates[newState] = pathCost
                steps.push([(newState, successor[1], pathCost), step], estimatedCost)

    # Goal not found
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
