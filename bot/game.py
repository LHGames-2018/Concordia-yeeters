actions = {0:'left', 1:'right', 2:'up', 3:'down', 4:'mine'}
from foundry import Foundry

class Game(Foundry):
	
    def __init__(self, grid_size=20):
        self.grid_size = grid_size
        self.reset()
        self.state_changed = True

	@property
	def name(self):
		return "LH"
	
	@property
	def nb_actions(self):
		return 5
	
	def reset(self):
		pass

    def play(self, action):
        assert action in range(5), "Invalid action."
        self.scored = False
        self.move_snake(action)

	def get_state(self):
		return None

	def get_score(self):
		return 0

	def is_over(self):
		return False

	def is_won(self):
		return False

	def get_frame(self):
		return self.get_state()

	def draw(self):
		return self.get_state()

	def get_possible_actions(self):
		return range(self.nb_actions)
