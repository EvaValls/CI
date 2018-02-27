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

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        currentPos = currentGameState.getPacmanPosition()

        "*** YOUR CODE HERE ***"
        foodList = newFood.asList() 
        foodDist = []
        ghostDist =[]

        if not foodList:
          # si no queda menjar retornem maxim
          return 9999
        else:
          # calculem distancies a tot el menjar
          for food in foodList:
            foodDist.append(util.manhattanDistance( newPos, food ))

        for ghost in newGhostStates:
          # calculem distancies als fantasmes
          ghostPos = ghost.getPosition()
          ghostDist.append(util.manhattanDistance(newPos, ghostPos ))
        
        # retornem score + fantasma mes proper - menjar mes proper
        return successorGameState.getScore() + min(ghostDist) - min(foodDist)


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

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        ghosts = gameState.getNumAgents()-1
        bestVal = float("-inf")
        bestAct = None
        #primer agent es el pacman. Pacman maximitza. (getMax) Pacman = MAX
        #els seguents son els fantasmes. Fantasmes minimitzen. (getMin) Cada fantasma = un nivell MIN
        #per agafem el valor mes gran dels nodes successors: la millor accio sera la que vaig al node amb el valor mes alt
        #per cada node successor obtenim els valors minims
        for action in gameState.getLegalActions(self.index):
          successor = gameState.generateSuccessor(self.index, action)
          val = max(bestVal, self.getMin( successor, self.index+1, self.depth, ghosts))
          if val> bestVal:
            bestVal, bestAct = val, action
        return bestAct
        util.raiseNotDefined()

    def getMax(self, successor, index,  depth, ghosts):

      actions = successor.getLegalActions(index)
      #si no te accions = node terminal. si depth=0 no s'ha d'expandir mes. Retornem valor del node
      if actions==[] or depth== 0 :
        return self.evaluationFunction(successor)
      bestVal = float("-inf")  
      for action in actions:
        succ = successor.generateSuccessor(index, action) 
        val = max(bestVal,self.getMin(succ, index+1, depth, ghosts))
        if val> bestVal:
          bestVal= val
      return bestVal

    def getMin(self, successor, index,  depth, ghosts):
      actions = successor.getLegalActions(index)
      if actions==[] or depth== 0 :
        return self.evaluationFunction(successor)
      bestVal = float("inf")  
      for action in actions:
        succ = successor.generateSuccessor(index, action)
        if index==ghosts:
          val = min(bestVal,self.getMax( succ, 0, depth-1, ghosts))
        else:
          val = min(bestVal,self.getMin( succ, index+1, depth, ghosts))
        if val < bestVal:
          bestVal= val
      return bestVal  

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        ghosts = gameState.getNumAgents()-1
        bestVal = float("-inf")
        bestAct = None
        alpha = float("-inf")
        beta = float("inf")
         
        for action in gameState.getLegalActions(self.index):
          successor = gameState.generateSuccessor(self.index, action)
          val = max(bestVal, self.getMin( successor, self.index+1, self.depth, ghosts, alpha, beta))
          if val > bestVal:
            bestVal = val
          #pacman es max --> actualitzem alpha
          if bestVal > alpha:
            alpha, bestAct = bestVal, action
        return bestAct
        util.raiseNotDefined()

    def getMax(self, successor, index,  depth, ghosts, bestAlp, bestBeta):

      actions = successor.getLegalActions(index)
      
      if actions==[] or depth== 0 :
        return self.evaluationFunction(successor)
      bestVal = float("-inf")  

      for action in actions:
        succ = successor.generateSuccessor(index, action) 
        val = max(bestVal,self.getMin(succ, index+1, depth, ghosts, bestAlp, bestBeta))
        if val > bestVal:
          bestVal = val
        #per max actualitzem el valor d'alpha
        if bestVal > bestAlp:
          bestAlp = bestVal
        #si el valor es superior a beta no cal seguir buscant
        if bestVal > bestBeta:
          break
      return bestVal

    def getMin(self, successor, index,  depth, ghosts, bestAlp, bestBeta):

      actions = successor.getLegalActions(index)
      if actions==[] or depth== 0 :
        return self.evaluationFunction(successor)
      bestVal = float("inf")
      for action in actions:
        succ = successor.generateSuccessor(index, action)
        if index==ghosts:
          val = min(bestVal,self.getMax( succ, 0, depth-1, ghosts, bestAlp, bestBeta))
        else:
          val = min(bestVal,self.getMin( succ, index+1, depth, ghosts, bestAlp, bestBeta))
        if val < bestVal:
          bestVal = val
        #per min actualitzem el valor de beta
        if bestVal < bestBeta:
          bestBeta = bestVal
        #si el valor es superior a alpha no cal seguir buscant
        if bestVal < bestAlp:
          break
      return bestVal

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

