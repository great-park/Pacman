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
    "*** YOUR CODE HERE ***"
    #초기화 작업
    startNode = problem.getStartState()
    firstRoute = []
    visitedNode = []
    fringe = util.Stack()
    fringe.push((startNode, firstRoute))

    #스택이 빌 때 까지
    while not fringe.isEmpty():
        Node, Route = fringe.pop()
        visitedNode.append(Node)
        #목표 지점에 도달할 때 까지
        if problem.isGoalState(Node):
            return Route
        #successor 가져오기
        for successor, move, cost in problem.getSuccessors(Node):
            if not successor in visitedNode:
                fringe.push((successor, Route + [move]))
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #초기화 작업, 큐 사용
    startNode = problem.getStartState()
    firstRoute = []
    visitedNode = []
    fringe = util.Queue()

    fringe.push((startNode, firstRoute))

    #큐가 빌 때 까지
    while not fringe.isEmpty():
        Node, Route = fringe.pop()

        if problem.isGoalState(Node):
            return Route
        #successor 가져오기
        for successor, move, cost in problem.getSuccessors(Node):
            if not successor in visitedNode:
                fringe.push((successor, Route + [move]))
                visitedNode.append(successor)
        visitedNode.append(Node)
    return []



def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #우선순위 큐 -> cost 이용
    startNode = problem.getStartState()
    firstRoute = []
    visitedNode = dict()
    fringe = util.PriorityQueue()

    fringe.push((startNode, firstRoute, 0), 0)

    while not fringe.isEmpty():
        Node, Route, Cost = fringe.pop()
        visitedNode[Node] = Cost

        if problem.isGoalState(Node):
            return Route

        for successor, move, current_cost in problem.getSuccessors(Node):
            #비용이 더 적거나, 아예 방문한 적이 없을 때 추가
            if ((successor in visitedNode) and (visitedNode[successor] > current_cost + Cost)) or (successor not in visitedNode):
                visitedNode[successor]= current_cost + Cost
                fringe.push((successor,Route + [move], current_cost + Cost), current_cost + Cost)

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
    #휴리스틱 함수 -> (state, 자기 자신의 정보) // F=G+H

    startNode = problem.getStartState()
    firstRoute = []
    visitedNode = dict()
    fringe = util.PriorityQueue()

    fringe.push((startNode, firstRoute, 0), 0+(heuristic(startNode, problem)))

    while not fringe.isEmpty():
        Node, Route, Cost = fringe.pop()
        visitedNode[Node] = Cost

        #탈출
        if problem.isGoalState(Node):
            return Route

        for successor, move, current_cost in problem.getSuccessors(Node):
            #UCS에서 heuristic function 추가하기 F=G+H, (state, 자기 자신의 정보)
            if ((successor in visitedNode) and (visitedNode[successor] > current_cost + Cost + (heuristic(successor, problem)))) \
                    or (successor not in visitedNode):
                visitedNode[successor] = current_cost + Cost
                fringe.push((successor, Route + [move], current_cost + Cost), current_cost + Cost + (heuristic(successor, problem)))

    return []



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
