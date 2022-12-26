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
    return [s, s, w, s, w, w, s, w]


class Path(object):
    def __init__(self, locations, directions, cost):
        self.locations = locations
        self.directions = directions
        self.cost = cost


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0



def manhattanHeuristic(position, problem, info={}):
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def aStarSearch(problem, heuristic=nullHeuristic):

    path = Path([problem.getStartState()], [], 0)

    queue = util.PriorityQueue()
    queue.push(path, 0)
    visited = [problem.getStartState()]

    while not queue.isEmpty():
        curPath = queue.pop()
        curLoc = curPath.locations[-1]
        if problem.isGoalState(curLoc):
            return curPath.directions
        else:
            nextSteps = problem.getSuccessors(curLoc)
            for step in nextSteps:
                nextLoc = step[0]
                nextDir = step[1]
                nextCost = step[2]
                if (nextLoc not in curPath.locations) and (nextLoc not in visited):
                    if not problem.isGoalState(nextLoc):
                        visited.append(nextLoc)
                    newLocs = curPath.locations[:]
                    newLocs.append(nextLoc)
                    newDirs = curPath.directions[:]
                    newDirs.append(nextDir)
                    newCosts = curPath.cost + nextCost
                    newPath = Path(newLocs, newDirs, newCosts)
                    queue.push(newPath, newCosts +
                               heuristic(nextLoc, problem))

    return []


def greedHeuristic(position, problem, info={}):
    xy1 = position
    xy2 = problem.goal
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5 #піфагор


def greedySearch(problem, heuristic=greedHeuristic):

    path = Path([problem.getStartState()], [], 0)

    queue = util.PriorityQueue()
    queue.push(path, 0)
    visited = [problem.getStartState()]

    while not queue.isEmpty():
        curPath = queue.pop()
        curLoc = curPath.locations[-1]
        if problem.isGoalState(curLoc):
            return curPath.directions
        else:
            nextSteps = problem.getSuccessors(curLoc)
            for step in nextSteps:
                nextLoc = step[0]
                nextDir = step[1]
                nextCost = step[2]
                if (nextLoc not in curPath.locations) and (nextLoc not in visited):
                    if not problem.isGoalState(nextLoc):
                        visited.append(nextLoc)
                    newLocs = curPath.locations[:]
                    newLocs.append(nextLoc)
                    newDirs = curPath.directions[:]
                    newDirs.append(nextDir)
                    newCosts = heuristic(nextLoc, problem)
                    newPath = Path(newLocs, newDirs, newCosts)
                    queue.push(newPath, newCosts)

    return []

    

def leeSearch(problem):

    path = Path([problem.getStartState()], [], 0)

    queue = util.PriorityQueue()
    queue.push(path, 0)
    visited = [problem.getStartState()]

    # BFS
    while not queue.isEmpty():
        curPath = queue.pop()
        curLoc = curPath.locations[-1]
        if problem.isGoalState(curLoc):
            return curPath.directions
        else:
            nextSteps = problem.getSuccessors(curLoc)
            for step in nextSteps:
                nextLoc = step[0]
                nextDir = step[1]
                nextCost = step[2]
                if (nextLoc not in curPath.locations) and (nextLoc not in visited):
                    if not problem.isGoalState(nextLoc):
                        visited.append(nextLoc)

                    newLocs = curPath.locations[:]
                    newLocs.append(nextLoc)

                    newDirs = curPath.directions[:]
                    newDirs.append(nextDir)

                    newCost = curPath.cost + nextCost
                    newPath = Path(newLocs, newDirs, newCost)
                    queue.push(newPath, newCost + 1)

    return []


# Abbreviations
lee = leeSearch
astar = aStarSearch
greed = greedySearch