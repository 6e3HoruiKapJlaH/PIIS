import chess
import numpy as np
from collections import defaultdict

class MonteCarloTreeSearchNode():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return
    
    def untried_actions(self):
        self._untried_actions = self.get_legal_actions()
        return self._untried_actions
    
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses
    
    def n(self):
        return self._number_of_visits
    
    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node 

    def is_terminal_node(self):
        return self.is_game_over()
    
    def rollout(self):
        import copy
        current_rollout_state = (self)
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = current_rollout_state.rollout_policy(possible_moves)
            current_rollout_state.state = current_rollout_state.move(action)
        return current_rollout_state.game_result()   
    
    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)
            
    def is_fully_expanded(self):
        return len(self._untried_actions) == 0       
         
    def best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)], self.children[np.argmax(choices_weights)].parent_action
    
    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]
    
    def _tree_policy(self):

        current_node = self
        while not current_node.is_terminal_node():
            
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node, a = current_node.best_child()
        return current_node
    
    def best_action(self):
        simulation_no = 100
        
        
        for i in range(simulation_no):
            
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        
        return self.best_child(c_param=.10)
    
    def get_legal_actions(self): 
        a = str(self.state.legal_moves).replace(")", "").replace(">", "").split(', ')
        if len(a)<=0:
            return a
        a[0] = a[0][a[0].find("(")+1:]
        return a
     
    def is_game_over(self):
        return self.state.is_game_over()
    def game_result(self):
        if self.state.result() == '0 - 1':
            return -1
        elif self.state.result() == '1 - 0':
            return 1
        else:
            return 0
    def move(self,action):
        import copy
        k = copy.deepcopy(self.state)
        k.push_san(san=action)
        """ self.state.push_san(san=action)
        k=self.state """
        return k
        
    
def main(initial_state):
    root = MonteCarloTreeSearchNode(state = initial_state)
    selected_node, a = root.best_action()
    board.push_san(san=a)
    print(board.turn)
    print(a)
    return selected_node
    

board = chess.Board('1r6/2bn1p1p/p1k2p2/3Rp3/PPP5/1N2P3/4KPPP/8 w KQkq - 0 1')
board.turn = True

while board.is_game_over() == False:
    initial_state = board
    a = main(initial_state)
    print(board)
    a = input("Input move: ")
    legal_moves = str(board.legal_moves).replace(")", "").replace(">", "").split(', ')
    legal_moves[0] = legal_moves[0][legal_moves[0].find("(")+1:]
    while a not in legal_moves:
        print("Illegal move")
        print(legal_moves)

        a = input("Input move: ")
    board.push_san(san=a)
    print(board)
    
print(board.result())
