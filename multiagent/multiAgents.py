# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.
    """
    def getAction(self, gameState):
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPosition = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = 0
        curFood = currentGameState.getFood()
        ghostPosition = successorGameState.getGhostPositions()

        foodDistance = list()
        ghostDistance = list()

        #맨하튼 distance!
        for food in newFood.asList():
            distance = manhattanDistance(food, newPosition)
            foodDistance.append(distance)
        for ghost in ghostPosition:
            distance = manhattanDistance(ghost, newPosition)
            ghostDistance.append(distance)

        newFoodDistance = float("inf")
        newGhostDistance = float("inf")

        for foodDistanceItem in foodDistance:
            newFoodDistance = min([newFoodDistance, foodDistanceItem])
        for ghostDistanceItem in ghostDistance:
            newGhostDistance = min([newGhostDistance, ghostDistanceItem])

        #음식 먹을 때 점수 부여
        if curFood[newPosition[0]][newPosition[1]]:
            score +=10

        #충돌 시 감점
        if newGhostDistance < 2:
            score -= 1000

        score = score + 1.0/newFoodDistance

        return score



def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    "*** YOUR CODE HERE ***"
    def min_value(self, gameState, depth, agent):
        actions = gameState.getLegalActions(agent)
        score = list()

        for action in actions:
            successorGameState = gameState.generateSuccessor(agent, action)

            #마지막 유령일 경우
            if agent == gameState.getNumAgents() -1:
                min_score = self.MiniMax(successorGameState, depth -1,agent=0, maximizing=True)[0]
                score.append(min_score)
            else:
                min_score = self.MiniMax(successorGameState, depth, agent=agent + 1, maximizing=False)[0]
                score.append(min_score)
        min_score = min(score)
        min_id = [i for i, score in enumerate(score) if score == min_score]

        finalAction = actions[random.choice(min_id)]
        return (min_score, finalAction)

    def max_value(self, gameState, depth, agent):
        actions = gameState.getLegalActions(agent)
        score = list()

        for action in actions:
            succssorGameState = gameState.generateSuccessor(agent, action)
            max_score = self.MiniMax(succssorGameState, depth,agent=agent + 1, maximizing=False)[0]
            score.append(max_score)

        max_score = max(score)
        max_id = [i for i, score in enumerate(score) if score == max_score]

        finalAction = actions[random.choice(max_id)]
        return (max_score, finalAction)

    def MiniMax(self, gameState, depth, agent = 0, maximizing = True):
        #끝
        if gameState.isWin() or gameState.isLose() or depth ==0:
            return self.evaluationFunction(gameState), Directions.STOP
        if maximizing:
            return self.max_value(gameState, depth, agent)
        else:
            return self.min_value(gameState, depth, agent)

    def getAction(self, gameState):
        finalAction = self.MiniMax(gameState, self.depth)[1]
        return finalAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    "*** YOUR CODE HERE ***"
    def getAction(self, gameState):
        a = -(float("inf"))
        b = float("inf")


        def min_value(gameState, agentId, depth, a, b):
            actions = gameState.getLegalActions(agentId)
            if len(actions) == 0:
                return self.evaluationFunction(gameState), None

            value = float("inf")
            move = None

            for action in actions:
                if (agentId == gameState.getNumAgents() - 1):
                    temp = max_value(gameState.generateSuccessor(agentId, action), depth +1, a, b)[0]
                else:
                    temp = min_value(gameState.generateSuccessor(agentId, action), agentId + 1, depth, a, b)[0]

                if (temp < value):
                    value, move = temp, action

                if (value < a):
                    return value, move

                b = min(b, value)

            return value, move

        def max_value(gameState, depth, a, b):
            actions = gameState.getLegalActions()
            if len(actions) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None
            value = float("-inf")
            move = None

            for action in actions:
                temp = min_value(gameState.generateSuccessor(0, action), 1, depth, a, b)[0]
                if (value < temp):
                    value, move = temp, action
                if (value > b):
                    return value, move
                a = max(a, value)

            return value, move

        move = max_value(gameState, 0, a, b)[1]
        return move

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()




def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
